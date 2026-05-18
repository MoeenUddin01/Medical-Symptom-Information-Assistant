import { useState } from 'react';
import SymptomInput from '../components/SymptomInput';
import EmergencyBanner from '../components/EmergencyBanner';
import ConditionCard from '../components/ConditionCard';
import Disclaimer from '../components/Disclaimer';
import LoadingState from '../components/LoadingState';
import fetchSymptomAnalysis from '../api/symptoms';

function Home() {
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

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

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-3xl mx-auto space-y-6">
        <div className="text-center space-y-1">
          <h1 className="text-3xl font-bold text-gray-900">MedAssist</h1>
          <p className="text-gray-500">Symptom Information Assistant</p>
        </div>

        <Disclaimer />

        <div className="bg-white rounded-lg shadow-sm p-6">
          <SymptomInput onSubmit={handleSubmit} isLoading={isLoading} />
        </div>

        {isLoading && <LoadingState />}

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <p className="text-red-700 text-sm">{error}</p>
          </div>
        )}

        {results && results.is_emergency && (
          <EmergencyBanner message={results.emergency_message} />
        )}

        {results && !results.is_emergency && results.conditions && results.conditions.length > 0 && (
          <div className="space-y-4">
            <h2 className="text-lg font-semibold text-gray-900">Possible Conditions</h2>
            {results.conditions.map((condition, index) => (
              <ConditionCard key={index} condition={condition} />
            ))}
          </div>
        )}

        {results && !results.is_emergency && results.conditions && results.conditions.length === 0 && (
          <div className="bg-gray-100 rounded-lg p-6 text-center">
            <p className="text-gray-600">No matching conditions found. Please consult a healthcare professional.</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Home;