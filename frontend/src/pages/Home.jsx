import { useState } from 'react';
import SymptomInput from '../components/SymptomInput';
import EmergencyBanner from '../components/EmergencyBanner';
import ConditionCard from '../components/ConditionCard';
import Disclaimer from '../components/Disclaimer';
import LoadingState from '../components/LoadingState';
import fetchSymptomAnalysis from '../api/symptoms';

const QUICK_SUGGESTIONS = [
  { text: "I have had a severe throbbing headache for two days, feeling nauseous and sensitive to light.", label: "Migraine" },
  { text: "My temperature is 38.5°C with a persistent dry cough, body aches, and fatigue.", label: "Fever & Dry Cough" },
  { text: "I developed an itchy red rash with small blister-like bumps on my left arm.", label: "Itchy Rash" },
  { text: "I feel dizzy, lightheaded when standing, and have a spinning vertigo sensation.", label: "Vertigo / Dizziness" }
];

function Home() {
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [prefilledText, setPrefilledText] = useState('');

  const handleSubmit = async (text) => {
    setIsLoading(true);
    setError(null);
    setResults(null);
    try {
      const data = await fetchSymptomAnalysis(text);
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSuggestionClick = (suggestionText) => {
    setPrefilledText(suggestionText);
  };

  return (
    <div className="min-h-screen bg-slate-50/20 py-8 px-6">
      <div className="max-w-3xl mx-auto space-y-6">
        
        {/* Evidence AI Landing Header Card */}
        <div className="bg-gradient-to-tr from-teal-900 via-teal-800 to-cyan-950 rounded-3xl p-8 text-white relative overflow-hidden shadow-xl shadow-teal-950/15">
          <div className="absolute right-0 top-0 -mr-16 -mt-16 w-64 h-64 bg-teal-500/10 rounded-full blur-3xl"></div>
          <div className="absolute left-1/4 bottom-0 -ml-16 -mb-16 w-48 h-48 bg-cyan-500/5 rounded-full blur-3xl"></div>
          
          <div className="relative z-10 space-y-3.5 max-w-xl">
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[11px] font-bold tracking-wide uppercase bg-teal-500/20 text-teal-200 backdrop-blur-sm border border-teal-500/20">
              <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 01-1.043 3.296 3.745 3.745 0 01-3.296 1.043A3.745 3.745 0 0110 20.062a3.745 3.745 0 01-3.296-1.043 3.745 3.745 0 01-1.043-3.296A3.748 3.748 0 013 12c0-1.268.63-2.39 1.593-3.068a3.745 3.745 0 011.043-3.296 3.746 3.746 0 013.296-1.043A3.746 3.746 0 0110 3.938a3.745 3.745 0 013.296 1.043 3.745 3.745 0 011.043 3.296A3.748 3.748 0 0121 12z" />
              </svg>
              Grounded Evidence-Based AI
            </span>
            <h1 className="text-3xl font-extrabold tracking-tight font-outfit text-white leading-tight md:text-4xl">
              Evidence-based <br /><span className="bg-gradient-to-r from-teal-300 to-cyan-200 bg-clip-text text-transparent">symptom intelligence</span>
            </h1>
            <p className="text-teal-100/85 text-sm md:text-[15px] font-normal leading-relaxed">
              Describe your symptoms below. MedAssist AI cross-references verified WHO and NHS medical repositories in real time to generate clinically grounded condition insights.
            </p>
          </div>
        </div>

        {/* Disclaimer Notice */}
        <Disclaimer />

        {/* Symptoms Form Card */}
        <div className="bg-white rounded-3xl border border-slate-100 shadow-sm p-6 md:p-8 premium-glow space-y-6">
          <SymptomInput onSubmit={handleSubmit} isLoading={isLoading} prefilledText={prefilledText} />

          {/* Quick-Start Suggestions */}
          {!isLoading && (
            <div className="space-y-2.5 pt-4 border-t border-slate-100">
              <p className="text-xs font-bold text-slate-500 tracking-wider uppercase font-outfit">
                Quick-Start Suggestions
              </p>
              <div className="flex flex-wrap gap-2">
                {QUICK_SUGGESTIONS.map((suggestion, index) => (
                  <button
                    key={index}
                    type="button"
                    onClick={() => handleSuggestionClick(suggestion.text)}
                    className="px-3.5 py-2 rounded-xl text-xs font-semibold bg-slate-50 hover:bg-teal-50 hover:text-teal-700 text-slate-600 border border-slate-200/60 hover:border-teal-200 transition-all duration-300 active:scale-[0.98]"
                  >
                    {suggestion.label}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Active Analysis Loader */}
        {isLoading && <LoadingState />}

        {/* Error Notification */}
        {error && (
          <div className="bg-red-50 border border-red-200/80 rounded-2xl p-4 flex gap-3 items-start premium-glow">
            <svg className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
            <div className="space-y-1">
              <p className="text-sm font-bold text-red-800">Connection Interrupted</p>
              <p className="text-xs text-red-700 leading-normal">{error}</p>
            </div>
          </div>
        )}

        {/* Emergency Banner */}
        {results && results.is_emergency && (
          <EmergencyBanner message={results.emergency_message} />
        )}

        {/* Recommendations / Conditions list */}
        {results && !results.is_emergency && results.conditions && results.conditions.length > 0 && (
          <div className="space-y-4 pt-2">
            <div className="flex items-center justify-between px-2">
              <h2 className="text-lg font-bold text-slate-800 font-outfit">Possible Conditions</h2>
              <span className="text-xs font-semibold text-slate-500 bg-slate-100 px-2.5 py-1 rounded-full">
                {results.conditions.length} match{results.conditions.length !== 1 ? 'es' : ''} identified
              </span>
            </div>
            <div className="grid gap-4">
              {results.conditions.map((condition, index) => (
                <ConditionCard key={index} condition={condition} />
              ))}
            </div>
          </div>
        )}

        {/* Empty state (Should not hit due to backend fallback, but kept as safety) */}
        {results && !results.is_emergency && results.conditions && results.conditions.length === 0 && (
          <div className="bg-slate-50 border border-slate-100 rounded-3xl p-8 text-center premium-glow">
            <svg className="w-12 h-12 text-slate-300 mx-auto mb-3" fill="none" stroke="currentColor" strokeWidth="1.5" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
            </svg>
            <p className="text-sm font-semibold text-slate-600">No matching medical reference conditions identified.</p>
            <p className="text-xs text-slate-500 mt-1 leading-normal">
              Always consult a medical professional for appropriate clinical assessment and diagnosis.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Home;