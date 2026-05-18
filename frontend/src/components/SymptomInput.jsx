import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

function SymptomInput({ onSubmit, isLoading, prefilledText }) {
  const [text, setText] = useState('');
  const [error, setError] = useState('');

  // Sync prefilled text from parent (for quick suggestion tags)
  useEffect(() => {
    if (prefilledText) {
      setText(prefilledText);
      setError('');
    }
  }, [prefilledText]);

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
  };

  return (
    <form onSubmit={handleSubmit} className="w-full space-y-4">
      <div className="flex flex-col space-y-1.5">
        <label htmlFor="symptoms" className="text-sm font-bold text-slate-700 tracking-wide uppercase font-outfit">
          Describe your symptoms in plain language
        </label>
        <p className="text-xs text-slate-500">
          Provide as much detail as possible (duration, severity, triggers, accompanying symptoms) for better matching.
        </p>
      </div>

      <div className="relative group">
        <textarea
          id="symptoms"
          value={text}
          onChange={(e) => {
            setText(e.target.value);
            if (e.target.value.trim().length >= 3) {
              setError('');
            }
          }}
          disabled={isLoading}
          placeholder="e.g. I have had a severe throbbing headache for 2 days, feeling nauseous and sensitive to light..."
          rows={4}
          className={`w-full px-5 py-4 rounded-xl border font-sans text-base transition-all duration-300 resize-none text-slate-800 placeholder-slate-400 bg-slate-50/50 ${
            isLoading 
              ? 'bg-slate-100/50 border-slate-200 cursor-not-allowed opacity-60' 
              : error 
                ? 'border-red-400 focus:border-red-500 focus:ring-4 focus:ring-red-100 bg-white' 
                : isNearLimit 
                  ? 'border-amber-400 focus:border-amber-500 focus:ring-4 focus:ring-amber-100 bg-white'
                  : 'border-slate-200/80 focus:border-teal-500 focus:ring-4 focus:ring-teal-100 bg-white hover:border-slate-300 shadow-sm'
          }`}
        />
      </div>

      <div className="flex justify-between items-center h-5">
        <span className={`text-xs font-semibold ${isNearLimit ? 'text-amber-500' : 'text-slate-400'}`}>
          {charCount}/1000 characters
        </span>
        {error && (
          <span className="text-xs font-bold text-red-600 flex items-center gap-1">
            <svg className="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            {error}
          </span>
        )}
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className={`w-full py-4 px-6 rounded-xl font-bold font-outfit text-white shadow-lg transition-all duration-300 flex items-center justify-center gap-2.5 ${
          isLoading
            ? 'bg-slate-300 text-slate-500 shadow-none cursor-not-allowed'
            : 'bg-gradient-to-r from-teal-600 to-cyan-600 hover:from-teal-700 hover:to-cyan-700 hover:shadow-teal-600/20 hover:scale-[1.01] active:scale-[0.99]'
        }`}
      >
        {isLoading ? (
          <>
            <svg className="animate-spin h-5 w-5 text-teal-600" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Analysing Medical Data...
          </>
        ) : (
          <>
            <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
            </svg>
            Analyse Symptoms
          </>
        )}
      </button>
    </form>
  );
}

SymptomInput.propTypes = {
  onSubmit: PropTypes.func.isRequired,
  isLoading: PropTypes.bool.isRequired,
  prefilledText: PropTypes.string,
};

export default SymptomInput;