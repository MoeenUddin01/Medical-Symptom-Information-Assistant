function LoadingState() {
  return (
    <div className="flex flex-col items-center justify-center py-8 space-y-4">
      <div className="relative w-16 h-16">
        <div className="absolute inset-0 rounded-full bg-blue-200 animate-pulse"></div>
        <div className="absolute inset-2 rounded-full bg-blue-300 animate-pulse animation-delay-150"></div>
        <div className="absolute inset-4 rounded-full bg-blue-400 animate-pulse animation-delay-300"></div>
      </div>
      <p className="text-gray-600 text-sm font-medium animate-pulse">Analysing your symptoms...</p>
    </div>
  );
}

export default LoadingState;