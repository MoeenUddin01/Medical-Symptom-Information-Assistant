import { useState } from 'react';
import PropTypes from 'prop-types';

function SymptomInput({ onSubmit, isLoading }) {
  const [text, setText] = useState('');
  const [error, setError] = useState('');

  const charCount = text.length;
  const isNearLimit = charCount > 900;

  const handleSubmit = (e) => {
    e.preventDefault();
    const trimmed = text.trim();
    if (trimmed.length < 3) {
      setError('Please describe your symptoms in at least 3 characters.');
      return;
    }
    setError('');
    onSubmit(trimmed);
    setText('');
  };

  return (
    <form onSubmit={handleSubmit} className="w-full space-y-2">
      <label htmlFor="symptoms" className="block text-sm font-medium text-gray-700">
        Describe your symptoms in plain language
      </label>
      <textarea
        id="symptoms"
        value={text}
        onChange={(e) => setText(e.target.value)}
        disabled={isLoading}
        placeholder="e.g. I have had a headache for 2 days, with mild fever and sensitivity to light..."
        rows={4}
        className={`w-full px-4 py-3 rounded-lg border ${isNearLimit ? 'border-red-400' : 'border-gray-300'} focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-colors resize-none text-gray-900 placeholder-gray-400 ${isLoading ? 'bg-gray-100 cursor-not-allowed' : ''}`}
      />
      <div className="flex justify-between items-center">
        <p className={`text-xs ${isNearLimit ? 'text-red-500' : 'text-gray-500'}`}>
          {charCount}/1000
        </p>
        {error && <p className="text-sm text-red-600">{error}</p>}
      </div>
      <button
        type="submit"
        disabled={isLoading}
        className={`w-full py-3 px-6 rounded-lg font-medium text-white transition-colors flex items-center justify-center gap-2 ${isLoading ? 'bg-blue-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'}`}
      >
        {isLoading ? (
          <>
            <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24" fill="none">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Analysing...
          </>
        ) : (
          'Analyse Symptoms'
        )}
      </button>
    </form>
  );
}

SymptomInput.propTypes = {
  onSubmit: PropTypes.func.isRequired,
  isLoading: PropTypes.bool.isRequired,
};

export default SymptomInput;