import time
import math
import re
from pathlib import Path

from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from backend.config import (
    CHROMA_DB_PATH,
    CHROMA_COLLECTION_NAME,
    EMBEDDING_MODEL,
    CHUNK_MIN_WORDS,
    CHUNK_MAX_WORDS,
    CHUNK_OVERLAP_WORDS,
)


MEDICAL_DOCUMENTS = [
    {
        "source": "WHO Headache Fact Sheet",
        "topic": "headache",
        "text": (
            "Headache is one of the most common disorders of the nervous system. "
            "It is a painful and disabling feature of a small number of primary headache disorders, "
            "namely migraine, tension-type headache, and cluster headache. "
            "Headache can also be caused by or occur secondarily to a long list of other conditions, "
            "the most common of which is medication-overuse headache. "
            "Worldwide, only a minority of people with headache disorders are diagnosed appropriately by a healthcare provider. "
            "Migraine is a primary headache disorder characterized by recurrent attacks of moderate to severe throbbing pain, "
            "typically on one side of the head, lasting 4 to 72 hours. "
            "The pain is often accompanied by nausea, vomiting, and sensitivity to light and sound. "
            "Some people experience an aura before the headache begins, which may include visual disturbances such as flashing lights or blind spots. "
            "Migraine affects approximately one in seven people worldwide and is more common in women than men. "
            "Tension-type headache is the most common primary headache disorder and is characterized by a pressing or tightening sensation "
            "around the head, often described as a band-like pressure. "
            "The pain is usually mild to moderate and does not worsen with physical activity. "
            "Tension-type headaches can last from 30 minutes to several days and are often associated with stress, fatigue, or poor posture. "
            "Cluster headache is a less common but extremely painful primary headache disorder. "
            "It occurs in cyclical patterns or clusters, with attacks of severe unilateral pain around the eye or temple. "
            "The pain is accompanied by autonomic symptoms such as tearing, nasal congestion, and restlessness. "
            "Individual attacks last 15 minutes to 3 hours and can occur several times a day. "
            "Medication-overuse headache occurs when acute headache medications are used too frequently, typically more than 10 to 15 days per month. "
            "It is the most common secondary headache disorder and can be reversed by withdrawing the overused medication. "
            "Treatment for headache disorders depends on the type and severity. "
            "Acute treatments include simple analgesics such as paracetamol or ibuprofen for mild to moderate pain, "
            "and triptans for moderate to severe migraine. "
            "Preventive treatments include beta-blockers, antidepressants, and anticonvulsants, "
            "which are taken regularly to reduce the frequency and severity of attacks. "
            "Lifestyle modifications such as regular sleep, adequate hydration, stress management, and avoiding trigger foods can also help. "
            "Anyone experiencing sudden severe headache unlike any before, headache with fever and stiff neck, "
            "headache after head injury, or headache accompanied by confusion or loss of consciousness should seek emergency medical attention immediately. "
            "Chronic daily headache is defined as headache occurring on 15 or more days per month for at least three months. "
            "Proper diagnosis requires a detailed headache diary and medical history review by a qualified healthcare professional."
        ),
    },
    {
        "source": "NHS Health A-Z — Fever",
        "topic": "fever",
        "text": (
            "A high temperature or fever is usually defined as a body temperature of 38 degrees Celsius or above. "
            "It is a common symptom of many conditions and is the body's natural response to infection. "
            "When the immune system detects an invading pathogen such as a virus or bacteria, "
            "it releases chemicals called pyrogens that signal the hypothalamus to raise the body's set point temperature. "
            "This elevated temperature helps the immune system fight infection more effectively "
            "by inhibiting the growth of pathogens and enhancing the activity of white blood cells. "
            "The most common causes of fever are viral infections such as influenza, the common cold, and COVID-19, "
            "as well as bacterial infections including urinary tract infections, strep throat, and pneumonia. "
            "Fever can also result from inflammatory conditions such as rheumatoid arthritis, "
            "heat exhaustion, certain medications, and vaccination. "
            "In most cases, a mild to moderate fever in an otherwise healthy adult does not require medical treatment. "
            "Rest and adequate fluid intake are the mainstays of management. "
            "Over-the-counter medications such as paracetamol or ibuprofen can reduce fever and relieve discomfort, "
            "but they do not treat the underlying cause. "
            "It is important to drink plenty of fluids to prevent dehydration, as fever increases fluid loss through sweating. "
            "Adults should seek medical advice if the fever persists for more than three days, "
            "reaches 40 degrees Celsius or higher, or is accompanied by severe headache, stiff neck, rash, difficulty breathing, or confusion. "
            "Children with fever require special attention. "
            "Parents should contact a healthcare provider if a child under three months has a temperature of 38 degrees or higher, "
            "or if a child aged three to six months has a temperature of 39 degrees or higher. "
            "Other warning signs in children include lethargy, irritability, poor feeding, dehydration, and seizures. "
            "Febrile seizures are convulsions triggered by fever in young children aged six months to five years. "
            "While frightening, most febrile seizures are brief and cause no long-term harm. "
            "Treatment involves placing the child on their side, not restraining them, and seeking medical evaluation after the seizure ends. "
            "Fever in adults should be monitored with a reliable thermometer. "
            "Oral, rectal, and tympanic thermometers provide the most accurate readings. "
            "Axillary or forehead measurements are less accurate but can be used for initial screening. "
            "It is important to note that the degree of fever does not always correlate with the severity of illness. "
            "A mild fever can accompany a serious infection and a high fever can occur with a minor illness. "
            "The overall clinical picture including other symptoms and the patient's general condition is more important than the temperature number alone."
        ),
    },
    {
        "source": "NHS Health A-Z — Cough",
        "topic": "cough",
        "text": (
            "A cough is a reflex action that clears the airways of mucus, irritants, and foreign particles. "
            "It is one of the most common reasons for medical consultations and can be classified as acute, subacute, or chronic. "
            "An acute cough lasts less than three weeks and is most commonly caused by upper respiratory tract infections such as the common cold, influenza, or acute bronchitis. "
            "A subacute cough persists for three to eight weeks and often follows a respiratory infection. "
            "A chronic cough lasts more than eight weeks and may indicate an underlying condition such as asthma, gastroesophageal reflux disease, or chronic obstructive pulmonary disease. "
            "Coughs can be productive, meaning they bring up mucus or phlegm, or dry and non-productive. "
            "A productive cough helps clear the lungs and should not be suppressed entirely. "
            "The color and consistency of the mucus can provide diagnostic clues: clear mucus is typical of viral infections, "
            "yellow or green mucus suggests bacterial infection, and rusty or blood-tinged mucus requires immediate medical evaluation. "
            "Common causes of acute cough include viral upper respiratory tract infections, which are typically self-limiting and resolve within one to three weeks. "
            "Treatment focuses on symptom relief with rest, adequate hydration, and honey for adults and children over one year of age. "
            "Over-the-counter cough medicines are not routinely recommended as evidence for their effectiveness is limited. "
            "Whooping cough or pertussis is a bacterial infection that causes severe coughing fits followed by a characteristic whooping sound during inhalation. "
            "It is preventable through vaccination and requires antibiotic treatment. "
            "Croup is a viral infection in young children that causes a barking cough and stridor, often worse at night. "
            "Steam inhalation and cool air can help relieve symptoms, but severe cases require medical attention. "
            "Chronic cough has several possible causes. "
            "Cough variant asthma presents with cough as the main symptom and responds to asthma treatments. "
            "Gastroesophageal reflux disease can cause cough due to stomach acid irritating the esophagus and airways. "
            "Post-nasal drip from sinusitis or allergies can trigger a persistent cough. "
            "Certain medications, particularly ACE inhibitors used for blood pressure, are known to cause chronic cough as a side effect. "
            "Smoking is a major cause of chronic cough and chronic bronchitis. "
            "Anyone with a cough that persists for more than three weeks, produces blood, is accompanied by chest pain, shortness of breath, or unexplained weight loss should see a doctor. "
            "A cough accompanied by high fever, difficulty breathing, or bluish skin or lips requires emergency attention. "
            "Preventive measures include hand hygiene, vaccination against influenza and pertussis, and avoiding exposure to tobacco smoke and other lung irritants."
        ),
    },
    {
        "source": "NHS Health A-Z — Rash",
        "topic": "rash",
        "text": (
            "A rash is an area of irritated, swollen, or abnormal skin that can appear in many forms including red patches, bumps, blisters, or scales. "
            "Rashes can be localized to one area of the body or widespread and can vary in appearance depending on the underlying cause. "
            "Common causes of rash include allergic reactions, infections, autoimmune disorders, and contact with irritants. "
            "Eczema or atopic dermatitis is a chronic inflammatory skin condition characterized by dry, itchy, and red skin. "
            "It often begins in childhood and is associated with other atopic conditions such as asthma and hay fever. "
            "Management includes regular moisturizing, avoiding triggers, and using topical corticosteroids during flare-ups. "
            "Contact dermatitis occurs when the skin comes into direct contact with an irritant or allergen. "
            "Common triggers include poison ivy, nickel, fragrances, and latex. "
            "The rash is usually confined to the area of contact and resolves once the irritant is removed. "
            "Urticaria or hives are raised, itchy welts that can appear suddenly as part of an allergic reaction. "
            "They are often caused by foods, medications, or insect stings and usually resolve within 24 hours. "
            "Antihistamines provide effective symptom relief for most cases. "
            "Fungal skin infections such as ringworm and athlete's foot cause red, scaly, and often ring-shaped rashes. "
            "They are treated with antifungal creams and maintaining good hygiene to prevent recurrence. "
            "Viral infections are a common cause of rashes in children. "
            "Chickenpox causes an itchy, blister-like rash that progresses through stages before crusting over. "
            "Measles presents with a red, blotchy rash that starts on the face and spreads downward, accompanied by fever, cough, and conjunctivitis. "
            "Hand, foot, and mouth disease causes a rash of small red spots and blisters on the hands, feet, and inside the mouth. "
            "Scarlet fever is a bacterial infection that causes a fine, sandpaper-like red rash and requires antibiotic treatment. "
            "Shingles is a reactivation of the chickenpox virus that causes a painful, blistering rash along a nerve pathway. "
            "It can be prevented with vaccination and treated with antiviral medications if started early. "
            "Cellulitis is a bacterial skin infection that causes red, swollen, warm, and tender skin, often with fever. "
            "It requires prompt antibiotic treatment to prevent spread to deeper tissues or the bloodstream. "
            "Petechiae are tiny red or purple spots on the skin that do not blanch when pressed and can indicate a serious condition such as meningitis or a bleeding disorder. "
            "A rash accompanied by fever, difficulty breathing, swelling of the face or throat, confusion, or rapid spread requires emergency medical attention. "
            "Meningitis rash does not fade when pressed under a glass and is a medical emergency. "
            "Treatment of rash depends entirely on the underlying cause, and self-diagnosis can be misleading. "
            "Any persistent, worsening, or painful rash should be evaluated by a healthcare professional for accurate diagnosis and appropriate management."
        ),
    },
    {
        "source": "NHS Health A-Z — Nausea and Vomiting",
        "topic": "nausea",
        "text": (
            "Nausea is an unpleasant sensation of feeling the need to vomit, often described as feeling sick to the stomach. "
            "Vomiting is the forceful expulsion of stomach contents through the mouth. "
            "Both are common symptoms of many conditions and are controlled by the vomiting center in the brainstem. "
            "The most common causes of nausea and vomiting include gastroenteritis or stomach flu, food poisoning, pregnancy especially morning sickness, "
            "motion sickness, migraine headaches, and side effects of medications such as chemotherapy drugs and opioids. "
            "Gastroenteritis is an infection of the digestive tract usually caused by viruses such as norovirus or rotavirus. "
            "It typically causes nausea, vomiting, diarrhea, and abdominal cramps and resolves within a few days with supportive care. "
            "The primary goal of management is preventing dehydration, especially in children and older adults. "
            "Small frequent sips of clear fluids such as water, oral rehydration solutions, or diluted juice are recommended. "
            "Ice chips or lollipops can help when even sips are not tolerated. "
            "Food should be reintroduced gradually with bland, easy-to-digest options such as crackers, toast, rice, and bananas. "
            "Ginger in various forms including ginger tea, ginger ale, or ginger supplements has been shown to reduce nausea. "
            "Peppermint tea or aromatherapy may also provide relief for mild nausea. "
            "Over-the-counter antiemetic medications such as meclizine or dimenhydrinate can help with motion sickness and mild nausea. "
            "Prescription antiemetics such as ondansetron are used for more severe cases including chemotherapy-induced nausea. "
            "Nausea and vomiting in pregnancy commonly occur during the first trimester. "
            "Most cases resolve by 16 to 20 weeks of gestation. "
            "Severe persistent vomiting in pregnancy called hyperemesis gravidarum requires medical treatment to prevent dehydration and nutritional deficiencies. "
            "Motion sickness occurs when the brain receives conflicting signals from the inner ear, eyes, and deeper body parts about motion. "
            "Prevention includes looking at a fixed point in the distance, avoiding reading while traveling, and taking anti-motion sickness medication before travel. "
            "Nausea can also be a symptom of more serious conditions including appendicitis, pancreatitis, gallbladder disease, intestinal obstruction, and heart attack. "
            "Vomiting that persists for more than 48 hours in adults or more than 24 hours in children requires medical evaluation. "
            "Signs of dehydration include dry mouth, decreased urination, dark urine, dizziness, and weakness. "
            "Severe dehydration requires intravenous fluid replacement in a medical setting. "
            "Vomiting blood or material that looks like coffee grounds, severe abdominal pain, stiff neck, high fever, or confusion accompanying nausea requires emergency care. "
            "Preventive measures include hand washing to reduce the risk of infectious causes, "
            "avoiding undercooked foods when traveling, and taking prescribed antiemetics before known triggers."
        ),
    },
    {
        "source": "NHS Health A-Z — Dizziness",
        "topic": "dizziness",
        "text": (
            "Dizziness is a term used to describe a range of sensations including feeling faint, lightheaded, weak, or unsteady. "
            "It is not a disease itself but a symptom of various underlying conditions. "
            "Dizziness can be classified into four main categories: vertigo, presyncope, disequilibrium, and lightheadedness. "
            "Vertigo is the sensation that you or your surroundings are spinning or moving. "
            "It is usually caused by problems in the inner ear or the vestibular nerve. "
            "Benign paroxysmal positional vertigo is the most common cause of vertigo and occurs when small calcium crystals become dislodged in the inner ear. "
            "It is triggered by changes in head position such as looking up or rolling over in bed. "
            "Treatment involves specific head and body maneuvers such as the Epley maneuver that reposition the crystals. "
            "Vestibular neuritis is an inflammation of the vestibular nerve often caused by a viral infection. "
            "It causes sudden severe vertigo lasting several days and is treated with vestibular suppressants and balance therapy. "
            "Meniere's disease is a disorder of the inner ear characterized by episodes of vertigo lasting 20 minutes to several hours, "
            "accompanied by tinnitus, hearing loss, and a feeling of fullness in the ear. "
            "Presyncope is the sensation of feeling faint or about to pass out, often caused by a temporary drop in blood flow to the brain. "
            "Common causes include dehydration, standing up too quickly, prolonged standing, and certain medications. "
            "Syncope is the actual loss of consciousness from reduced blood flow to the brain. "
            "Vasovagal syncope is the most common type, triggered by pain, fear, emotional distress, or straining. "
            "Disequilibrium is a feeling of being off-balance or unsteady when walking, often related to inner ear problems, "
            "neurological conditions such as Parkinson's disease or peripheral neuropathy, or musculoskeletal issues. "
            "It is more common in older adults and increases the risk of falls. "
            "Lightheadedness is a vague sensation of being disconnected from the environment, "
            "often associated with anxiety, hyperventilation, or side effects of medications. "
            "Diagnosis of the cause of dizziness requires a detailed history of the character, timing, and triggers of the episodes. "
            "Physical examination includes checking blood pressure lying and standing, eye movement tests, and balance assessments. "
            "Dizziness accompanied by chest pain, palpitations, severe headache, difficulty speaking, numbness or weakness on one side of the body, "
            "double vision, or loss of consciousness requires immediate emergency evaluation as these could indicate a stroke or heart condition. "
            "Most cases of dizziness resolve on their own or with treatment of the underlying cause. "
            "Self-care measures include moving slowly when changing positions, staying hydrated, avoiding caffeine and alcohol, "
            "and using handrails when available. "
            "Vestibular rehabilitation exercises can help retrain the brain to compensate for inner ear problems. "
            "Falls prevention is important for older adults with chronic dizziness and includes home safety modifications and balance training."
        ),
    },
]


def split_into_sentences(text: str):
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s.strip() for s in sentences if s.strip()]


def chunk_text(text: str, source: str, topic: str):
    sentences = split_into_sentences(text)
    chunks = []
    current_sentences = []
    current_word_count = 0
    overlap_sentences = []
    overlap_word_count = 0

    for sentence in sentences:
        sentence_word_count = len(sentence.split())
        current_sentences.append(sentence)
        current_word_count += sentence_word_count

        if current_word_count >= CHUNK_MIN_WORDS:
            chunks.append(" ".join(current_sentences))
            overlap_text = []
            overlap_count = 0
            for s in reversed(current_sentences):
                swc = len(s.split())
                if overlap_count + swc > CHUNK_OVERLAP_WORDS:
                    break
                overlap_text.insert(0, s)
                overlap_count += swc
            current_sentences = list(overlap_text)
            current_word_count = overlap_count

    if current_sentences:
        remaining = " ".join(current_sentences)
        if len(remaining.split()) > 50:
            chunks.append(remaining)

    chunk_objects = []
    for i, chunk in enumerate(chunks):
        chunk_objects.append(
            {
                "text": chunk,
                "metadata": {
                    "source": source,
                    "topic": topic,
                    "chunk_index": i,
                },
            }
        )

    return chunk_objects


def embed_and_store(chunks, model, collection):
    texts = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]
    ids = [
        f"{m['topic']}_{m['chunk_index']}_{int(time.time())}"
        for m in metadatas
    ]

    embeddings = model.encode(texts, show_progress_bar=True).tolist()

    collection.add(
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas,
        ids=ids,
    )

    return len(chunks)


def main():
    start_time = time.time()

    print("Loading embedding model...")
    model = SentenceTransformer(EMBEDDING_MODEL)

    print(f"Initializing ChromaDB at {CHROMA_DB_PATH}...")
    chroma_client = chromadb.PersistentClient(
        path=CHROMA_DB_PATH,
        settings=Settings(anonymized_telemetry=False),
    )
    collection = chroma_client.get_or_create_collection(
        name=CHROMA_COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    total_chunks = 0
    chunks_per_topic = {}

    for doc in MEDICAL_DOCUMENTS:
        topic = doc["topic"]
        print(f"Processing: {doc['source']} ({topic})...")
        doc_chunks = chunk_text(doc["text"], doc["source"], topic)
        count = embed_and_store(doc_chunks, model, collection)
        total_chunks += count
        chunks_per_topic[topic] = count
        print(f"  Stored {count} chunks for {topic}.")

    elapsed = time.time() - start_time

    print("\n" + "=" * 50)
    print("INGESTION COMPLETE")
    print("=" * 50)
    print(f"Total chunks stored: {total_chunks}")
    print("Chunks per topic:")
    for topic, count in chunks_per_topic.items():
        print(f"  {topic}: {count}")
    print(f"Time taken: {elapsed:.2f} seconds")
    print("=" * 50)


if __name__ == "__main__":
    main()
