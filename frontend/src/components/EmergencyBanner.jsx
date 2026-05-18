import PropTypes from 'prop-types';

function EmergencyBanner({ message }) {
  if (!message) {
    return null;
  }

  return (
    <div className="w-full bg-red-600 border-2 border-red-700 rounded-lg p-4 shadow-lg">
      <div className="flex items-center gap-4">
        <div className="relative flex-shrink-0">
          <span className="relative inline-flex h-5 w-5 rounded-full bg-red-500">
            <span className="absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75 animate-ping"></span>
          </span>
        </div>
        <div className="flex items-center gap-3">
          <svg
            className="w-8 h-8 text-white flex-shrink-0"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
            />
          </svg>
          <div>
            <p className="text-xl font-bold text-white">{message}</p>
            <p className="text-base text-red-100 mt-1">Call emergency services immediately — do not wait.</p>
          </div>
        </div>
      </div>
    </div>
  );
}

EmergencyBanner.propTypes = {
  message: PropTypes.string.isRequired,
};

export default EmergencyBanner;