import PropTypes from 'prop-types';
import SeverityBadge from './SeverityBadge';

function ConditionCard({ condition }) {
  const { name, explanation, severity, source } = condition;

  const accentBorder = {
    mild: 'before:bg-emerald-500',
    moderate: 'before:bg-amber-500',
    urgent: 'before:bg-rose-500'
  }[severity] || 'before:bg-slate-350';

  return (
    <div className={`relative overflow-hidden bg-white border border-slate-100 rounded-2xl shadow-sm hover:shadow-md transition-all duration-300 before:content-[""] before:absolute before:left-0 before:top-0 before:bottom-0 before:w-1.5 ${accentBorder}`}>
      <div className="p-5 space-y-4">
        {/* Header Block */}
        <div className="flex items-start justify-between gap-4">
          <div className="space-y-0.5">
            <h3 className="text-[17px] font-bold text-slate-800 font-outfit leading-tight tracking-tight">
              {name}
            </h3>
            <div className="flex items-center gap-1.5 text-[11px] font-semibold text-slate-400">
              <svg className="w-3.5 h-3.5 text-slate-400" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Clinical Reference Index
            </div>
          </div>
          <SeverityBadge severity={severity} />
        </div>

        {/* Content Divider */}
        <div className="h-[1px] bg-slate-100/70 w-full"></div>

        {/* Explanation Text */}
        <p className="text-slate-600 text-sm leading-relaxed font-normal">
          {explanation}
        </p>

        {/* Source Citation */}
        <div className="flex items-center gap-2 pt-0.5">
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-semibold bg-slate-50 text-slate-500 border border-slate-200/40 select-none">
            <svg className="w-3.5 h-3.5 text-slate-400" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582" />
            </svg>
            Verified Source: {source}
          </span>
        </div>
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