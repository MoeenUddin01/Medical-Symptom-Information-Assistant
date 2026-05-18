import { useState, useEffect } from 'react';

function LoadingState() {
  const [stage, setStage] = useState(0);
  const stages = [
    "Consulting NHS Health repositories...",
    "Querying WHO Headache & Pathology records...",
    "Validating semantic document matches...",
    "Synthesizing RAG facts via Llama-3.3..."
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setStage((prev) => (prev + 1) % stages.length);
    }, 1500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-white border border-slate-100 rounded-3xl p-8 premium-glow max-w-xl mx-auto space-y-6 text-center">
      {/* Moving Pulse Monitor Line */}
      <div className="relative w-full h-24 bg-slate-950 rounded-2xl overflow-hidden flex items-center justify-center border border-slate-900 shadow-inner">
        {/* ECG grid overlay */}
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#1e293b_1px,transparent_1px),linear-gradient(to_bottom,#1e293b_1px,transparent_1px)] bg-[size:16px_16px] opacity-40"></div>
        
        {/* Glowing sweep wave */}
        <div className="absolute left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-teal-400 to-transparent animate-ecg opacity-45"></div>
        
        {/* Heart Rate / Pulse SVG */}
        <svg className="w-4/5 h-16 text-teal-400 opacity-70 z-10" fill="none" viewBox="0 0 100 20" preserveAspectRatio="none">
          <path
            stroke="currentColor"
            strokeWidth="1.5"
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M0 10 h20 l2 -5 l2 10 l3 -16 l2 21 l2 -12 l2 2 h20 l2 -5 l2 10 l3 -16 l2 21 l2 -12 l2 2 h20"
          />
        </svg>
        
        {/* Live scanning pulse dot */}
        <span className="absolute top-4 right-4 flex h-2 w-2">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-teal-400 opacity-75"></span>
          <span className="relative inline-flex rounded-full h-2 w-2 bg-teal-400"></span>
        </span>
      </div>

      <div className="space-y-1.5">
        <h3 className="text-[11px] font-bold text-teal-600 tracking-widest uppercase font-outfit">
          AI Clinical Diagnostics Active
        </h3>
        <p className="text-slate-600 text-sm font-semibold animate-pulse transition-all duration-300">
          {stages[stage]}
        </p>
      </div>
    </div>
  );
}

export default LoadingState;