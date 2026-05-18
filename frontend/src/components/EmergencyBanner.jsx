import PropTypes from 'prop-types';

function EmergencyBanner({ message }) {
  if (!message) {
    return null;
  }

  return (
    <div className="w-full bg-gradient-to-tr from-rose-950 via-red-900 to-rose-900 border border-rose-900 rounded-3xl p-6 shadow-xl shadow-rose-950/15 text-white relative overflow-hidden premium-glow">
      {/* Background soft glow bubble */}
      <div className="absolute right-0 bottom-0 -mr-16 -mb-16 w-48 h-48 bg-rose-500/10 rounded-full blur-3xl"></div>
      
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6 relative z-10">
        <div className="flex items-start gap-4">
          <div className="relative mt-1 md:mt-0 flex-shrink-0">
            <span className="flex h-12 w-12 items-center justify-center rounded-2xl bg-white/10 text-rose-300 border border-white/10">
              <svg className="w-6 h-6 animate-pulse" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </span>
            <span className="absolute -top-1 -right-1 flex h-4.5 w-4.5">
              <span className="animate-pulse-ring absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-4.5 w-4.5 bg-rose-500 border-2 border-rose-950"></span>
            </span>
          </div>
          <div className="space-y-1.5 max-w-xl">
            <h4 className="text-[11px] font-extrabold text-rose-300 tracking-widest uppercase font-outfit">
              Critical Emergency Indicated
            </h4>
            <p className="text-xl font-extrabold tracking-tight text-white leading-tight font-outfit">
              {message}
            </p>
            <p className="text-rose-100/90 text-sm font-medium leading-relaxed">
              These symptoms warrant an immediate professional medical assessment. Call your local emergency dispatch (such as 911 or 999) or visit the nearest Emergency Room immediately. Do not delay care.
            </p>
          </div>
        </div>

        <a
          href="tel:911"
          className="w-full md:w-auto px-6 py-4 bg-white text-rose-900 font-bold font-outfit text-sm rounded-xl text-center shadow-lg shadow-rose-950/20 hover:bg-rose-50 active:scale-[0.98] transition-all duration-300 flex items-center justify-center gap-2 flex-shrink-0"
        >
          <svg className="w-4 h-4 flex-shrink-0 text-rose-700" fill="currentColor" viewBox="0 0 20 20">
            <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z" />
          </svg>
          Call Services (911 / 999)
        </a>
      </div>
    </div>
  );
}

EmergencyBanner.propTypes = {
  message: PropTypes.string.isRequired,
};

export default EmergencyBanner;