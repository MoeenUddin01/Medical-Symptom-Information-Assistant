function Disclaimer() {
  return (
    <div className="w-full bg-teal-50/50 border border-teal-150/60 rounded-2xl p-4 md:p-5 shadow-sm">
      <div className="flex items-start gap-3.5">
        <div className="relative flex-shrink-0 mt-0.5">
          {/* Animated active alert dot */}
          <span className="relative flex h-5 w-5 items-center justify-center">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-teal-400/50 opacity-75"></span>
            <svg className="w-5 h-5 text-teal-600 relative z-10" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M11.25 11.25l.041-.02a.75.75 0 111.063.852l-.708 2.836a.75.75 0 001.063.852l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z" />
            </svg>
          </span>
        </div>
        <div className="space-y-1">
          <h4 className="text-xs font-extrabold text-teal-800 tracking-wider uppercase font-outfit">
            Medical Advisory Notice
          </h4>
          <p className="text-xs md:text-sm text-teal-700/90 leading-relaxed font-medium">
            This assistant provides verified information for educational reference purposes only. It is **not a substitute for professional clinical judgment, diagnosis, or treatment**. Always consult a qualified healthcare provider for medical concerns.
          </p>
        </div>
      </div>
    </div>
  );
}

Disclaimer.propTypes = {};

export default Disclaimer;
