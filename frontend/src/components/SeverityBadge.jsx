import PropTypes from 'prop-types';

function SeverityBadge({ severity }) {
  const config = {
    mild: {
      bg: 'bg-green-100',
      text: 'text-green-800',
      dot: 'bg-green-500',
      label: 'Mild',
    },
    moderate: {
      bg: 'bg-amber-100',
      text: 'text-amber-800',
      dot: 'bg-amber-500',
      label: 'Moderate',
    },
    urgent: {
      bg: 'bg-red-100',
      text: 'text-red-700',
      dot: 'bg-red-500',
      label: 'Seek Care Urgently',
    },
  };

  const { bg, text, dot, label } = config[severity] || {
    bg: 'bg-gray-100',
    text: 'text-gray-700',
    dot: 'bg-gray-500',
    label: 'Unknown',
  };

  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${bg} ${text}`}>
      {severity === 'urgent' ? (
        <span className="relative flex h-2 w-2">
          <span className={`absolute inline-flex h-full w-full rounded-full ${dot} opacity-75 animate-ping`}></span>
          <span className={`relative inline-flex rounded-full h-2 w-2 ${dot}`}></span>
        </span>
      ) : (
        <span className={`h-2 w-2 rounded-full ${dot}`}></span>
      )}
      {label}
    </span>
  );
}

SeverityBadge.propTypes = {
  severity: PropTypes.oneOf(['mild', 'moderate', 'urgent']).isRequired,
};

export default SeverityBadge;