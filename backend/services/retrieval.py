"""
Knowledge retrieval module with local fallback.

This module handles querying the Supabase medical knowledge base
to retrieve relevant document chunks based on the user's symptom query.
If Supabase is offline, paused, or unreachable, it falls back to an
in-memory keyword search over verified medical reference documents.
"""

import logging
from typing import Dict, List

from backend.services.knowledge import search_knowledge, get_knowledge_count

logger = logging.getLogger(__name__)

# Fallback in-memory documents if Supabase is offline/paused
FALLBACK_DOCUMENTS = [
    {
        "source": "WHO Headache Fact Sheet",
        "topic": "headache",
        "text": "Headache is one of the most common disorders of the nervous system. It is a painful and disabling feature of a small number of primary headache disorders, namely migraine, tension-type headache, and cluster headache. Headache can also be caused by or occur secondarily to a long list of other conditions, the most common of which is medication-overuse headache. Migraine is a primary headache disorder characterized by recurrent attacks of moderate to severe throbbing pain, typically on one side of the head, lasting 4 to 72 hours. The pain is often accompanied by nausea, vomiting, and sensitivity to light and sound. Tension-type headache is the most common primary headache disorder and is characterized by a pressing or tightening sensation around the head, often described as a band-like pressure. The pain is usually mild to moderate and does not worsen with physical activity. Cluster headache is a less common but extremely painful primary headache disorder, causing severe unilateral pain around the eye or temple."
    },
    {
        "source": "NHS Health A-Z — Fever",
        "topic": "fever",
        "text": "A high temperature or fever is usually defined as a body temperature of 38 degrees Celsius or above. It is a common symptom of many conditions and is the body's natural response to infection. When the immune system detects an invading pathogen such as a virus or bacteria, it releases chemicals called pyrogens that signal the hypothalamus to raise the body's set point temperature. This elevated temperature helps the immune system fight infection more effectively by inhibiting the growth of pathogens and enhancing the activity of white blood cells. The most common causes of fever are viral infections such as influenza, the common cold, and COVID-19, as well as bacterial infections including urinary tract infections, strep throat, and pneumonia. Over-the-counter medications such as paracetamol or ibuprofen can reduce fever and relieve discomfort, but they do not treat the underlying cause."
    },
    {
        "source": "NHS Health A-Z — Cough",
        "topic": "cough",
        "text": "A cough is a reflex action that clears the airways of mucus, irritants, and foreign particles. It is one of the most common reasons for medical consultations and can be classified as acute, subacute, or chronic. An acute cough lasts less than three weeks and is most commonly caused by upper respiratory tract infections such as the common cold, influenza, or acute bronchitis. A subacute cough persists for three to eight weeks and often follows a respiratory infection. A chronic cough lasts more than eight weeks and may indicate an underlying condition such as asthma, gastroesophageal reflux disease (GERD), or chronic obstructive pulmonary disease (COPD). Coughs can be productive, meaning they bring up mucus or phlegm, or dry and non-productive. Treatment focuses on symptom relief with rest, adequate hydration, and honey."
    },
    {
        "source": "NHS Health A-Z — Rash",
        "topic": "rash",
        "text": "A rash is an area of irritated, swollen, or abnormal skin that can appear in many forms including red patches, bumps, blisters, or scales. Rashes can be localized to one area of the body or widespread and can vary in appearance depending on the underlying cause. Common causes of rash include allergic reactions, infections, autoimmune disorders, and contact with irritants. Eczema or atopic dermatitis is a chronic inflammatory skin condition characterized by dry, itchy, and red skin. Contact dermatitis occurs when the skin comes into direct contact with an irritant or allergen. Urticaria or hives are raised, itchy welts that can appear suddenly as part of an allergic reaction. Fungal skin infections such as ringworm and athlete's foot cause red, scaly, and often ring-shaped rashes."
    },
    {
        "source": "NHS Health A-Z — Nausea and Vomiting",
        "topic": "nausea",
        "text": "Nausea is an unpleasant sensation of feeling the need to vomit, often described as feeling sick to the stomach. Vomiting is the forceful expulsion of stomach contents through the mouth. Both are common symptoms of many conditions and are controlled by the vomiting center in the brainstem. The most common causes of nausea and vomiting include gastroenteritis or stomach flu, food poisoning, pregnancy especially morning sickness, motion sickness, migraine headaches, and side effects of medications. Gastroenteritis is an infection of the digestive tract usually caused by viruses such as norovirus or rotavirus. The primary goal of management is preventing dehydration. Small frequent sips of clear fluids such as water, oral rehydration solutions, or diluted juice are recommended. Ginger and peppermint can help relieve mild nausea."
    },
    {
        "source": "NHS Health A-Z — Dizziness",
        "topic": "dizziness",
        "text": "Dizziness is a term used to describe a range of sensations including feeling faint, lightheaded, weak, or unsteady. It is not a disease itself but a symptom of various underlying conditions. Dizziness can be classified into four main categories: vertigo, presyncope, disequilibrium, and lightheadedness. Vertigo is the sensation that you or your surroundings are spinning or moving, usually caused by problems in the inner ear or the vestibular nerve. Benign paroxysmal positional vertigo (BPPV) is the most common cause of vertigo. Presyncope is the sensation of feeling faint or about to pass out, often caused by a temporary drop in blood flow to the brain, common causes include dehydration and standing up too quickly. Disequilibrium is a feeling of being off-balance or unsteady when walking."
    }
]


def _local_fallback_search(query: str, n_results: int = 5) -> List[Dict]:
    """Perform a simple keyword-matching relevance search over in-memory documents."""
    logger.info(f"Executing local in-memory search fallback for query: '{query}'")
    keywords = [k.strip().lower() for k in query.split() if len(k.strip()) >= 3]
    
    results = []
    for doc in FALLBACK_DOCUMENTS:
        score = 0
        doc_text_lower = doc["text"].lower()
        doc_source_lower = doc["source"].lower()
        doc_topic_lower = doc["topic"].lower()
        
        for kw in keywords:
            if kw in doc_text_lower:
                score += 1
            if kw in doc_source_lower:
                score += 2
            if kw in doc_topic_lower:
                score += 3
                
        if score > 0:
            results.append({
                "text": doc["text"],
                "source": doc["source"],
                "topic": doc["topic"],
                "distance": max(0.1, 1.0 - (score / 15.0))
            })
            
    # Sort by relevance (lower distance is higher score)
    results.sort(key=lambda x: x["distance"])
    
    # If no matching keywords, return a default list of documents
    if not results:
        results = [
            {
                "text": doc["text"],
                "source": doc["source"],
                "topic": doc["topic"],
                "distance": 0.9
            }
            for doc in FALLBACK_DOCUMENTS
        ]
        
    return results[:n_results]


def retrieve_chunks(query: str, n_results: int = 5) -> List[Dict[str, str | float]]:
    """
    Retrieve relevant medical document chunks for a given query.

    Attempts to use Supabase, but falls back to local in-memory documents
    if Supabase is offline or returns empty results.
    """
    try:
        count = get_knowledge_count()
        if count == 0:
            logger.warning("Supabase medical_knowledge count is 0. Falling back to local search.")
            return _local_fallback_search(query, n_results)

        chunks = search_knowledge(query, limit=n_results)
        if not chunks:
            logger.warning("Supabase search returned no matches. Falling back to local search.")
            return _local_fallback_search(query, n_results)

        return chunks
    except Exception as e:
        logger.error(f"Failed to query Supabase: {str(e)}. Falling back to local search.")
        return _local_fallback_search(query, n_results)


def format_chunks_for_prompt(chunks: List[Dict[str, str | float]]) -> str:
    """
    Format retrieved chunks into a clean string for the LLM prompt.
    """
    if not chunks:
        return ""

    formatted_parts = []
    for i, chunk in enumerate(chunks, start=1):
        text = chunk.get("text", "").strip()
        source = chunk.get("source", "Unknown").strip()
        if text:
            formatted_parts.append(f"[{i}] Source: {source}\n{text}")

    return "\n\n".join(formatted_parts)