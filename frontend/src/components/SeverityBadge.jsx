import PropTypes from 'prop-types';

function SeverityBadge({ severity }) {
  const config = {
    mild: {
      bg: 'bg-emerald-50/80 text-emerald-800 border-emerald-100/80',
      dot: 'bg-emerald-500',
      label: 'Mild Severity',
      icon: (
        <svg className="w-3.5 h-3.5 text-emerald-600 flex-shrink-0" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      )
    },
    moderate: {
      bg: 'bg-amber-50/85 text-amber-800 border-amber-200/50',
      dot: 'bg-amber-500',
      label: 'Moderate Severity',
      icon: (
        <svg className="w-3.5 h-3.5 text-amber-600 flex-shrink-0" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
        </svg>
      )
    },
    urgent: {
      bg: 'bg-rose-50/90 text-rose-800 border-rose-200/50 ring-4 ring-rose-500/5',
      dot: 'bg-rose-500',
      label: 'Seek Care Urgently',
      icon: (
        <svg className="w-3.5 h-3.5 text-rose-600 flex-shrink-0" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
      )
    },
  };

  const active = config[severity] || {
    bg: 'bg-slate-50 text-slate-700 border-slate-200',
    dot: 'bg-slate-500',
    label: 'Evaluated Context',
    icon: null
  };

  return (
    <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold border transition-all duration-300 select-none ${active.bg}`}>
      {severity === 'urgent' ? (
        <span className="relative flex h-2 w-2">
          <span className={`absolute inline-flex h-full w-full rounded-full ${active.dot} opacity-75 animate-ping`}></span>
          <span className={`relative inline-flex rounded-full h-2 w-2 ${active.dot}`}></span>
        </span>
      ) : (
        <span className={`h-2 w-2 rounded-full ${active.dot}`}></span>
      )}
      {active.icon}
      {active.label}
    </span>
  );
}

SeverityBadge.propTypes = {
  severity: PropTypes.oneOf(['mild', 'moderate', 'urgent']).isRequired,
};

export default SeverityBadge;