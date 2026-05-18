import PropTypes from 'prop-types';

function Disclaimer() {
  return (
    <div className="w-full bg-blue-50 border-l-4 border-blue-400 rounded-r-lg p-4">
      <div className="flex items-start gap-3">
        <svg
          className="w-5 h-5 text-blue-500 flex-shrink-0 mt-0.5"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        <p className="text-sm text-blue-700 leading-relaxed">
          This tool is for information only and does not replace a doctor. Always consult a qualified healthcare professional for medical advice.
        </p>
      </div>
    </div>
  );
}

Disclaimer.propTypes = {};

export default Disclaimer;
