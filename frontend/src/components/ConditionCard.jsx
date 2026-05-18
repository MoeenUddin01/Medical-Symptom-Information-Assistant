import PropTypes from 'prop-types';
import SeverityBadge from './SeverityBadge';

function ConditionCard({ condition }) {
  const { name, explanation, severity, source } = condition;

  return (
    <div className="bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200">
      <div className="flex items-start justify-between p-4 pb-3">
        <h3 className="text-lg font-semibold text-gray-900">{name}</h3>
        <SeverityBadge severity={severity} />
      </div>
      <div className="border-t border-gray-200"></div>
      <div className="p-4">
        <p className="text-gray-700 leading-relaxed">{explanation}</p>
      </div>
      <div className="px-4 pb-4 flex items-center gap-2">
        <svg
          className="w-4 h-4 text-gray-400 flex-shrink-0"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
          />
        </svg>
        <p className="text-sm text-gray-500">Source: {source}</p>
      </div>
    </div>
  );
}

ConditionCard.propTypes = {
  condition: PropTypes.shape({
    name: PropTypes.string.isRequired,
    explanation: PropTypes.string.isRequired,
    severity: PropTypes.oneOf(['mild', 'moderate', 'urgent']).isRequired,
    source: PropTypes.string.isRequired,
  }).isRequired,
};

export default ConditionCard;