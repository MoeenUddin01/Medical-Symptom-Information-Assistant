import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom';
import Home from './pages/Home';
import History from './pages/History';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-slate-50/30 flex flex-col font-sans">
        {/* Glassmorphic Navbar */}
        <header className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-slate-100/90 premium-glow">
          <div className="max-w-4xl mx-auto px-6">
            <div className="flex items-center justify-between h-16">
              <NavLink to="/" className="flex items-center gap-2.5 group">
                <div className="relative flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-tr from-teal-500 to-cyan-500 shadow-md shadow-teal-500/10 group-hover:scale-105 transition-all duration-300">
                  <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12h15m0 0l-6.75-6.75M19.5 12l-6.75 6.75" />
                  </svg>
                  {/* Glowing ping indicator for AI active state */}
                  <span className="absolute -top-0.5 -right-0.5 flex h-2.5 w-2.5">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-400"></span>
                  </span>
                </div>
                <div className="flex flex-col">
                  <span className="text-lg font-bold text-slate-900 tracking-tight font-outfit leading-none">MedAssist</span>
                  <span className="text-[10px] font-semibold text-teal-600 tracking-widest uppercase mt-0.5 font-outfit">Evidence AI</span>
                </div>
              </NavLink>
              
              <nav className="flex items-center gap-1 bg-slate-100/60 p-1 rounded-xl">
                <NavLink
                  to="/"
                  className={({ isActive }) =>
                    `px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                      isActive
                        ? 'bg-white text-teal-700 shadow-sm font-semibold'
                        : 'text-slate-600 hover:text-slate-900 hover:bg-white/40'
                    }`
                  }
                >
                  Analyse Symptoms
                </NavLink>
                <NavLink
                  to="/history"
                  className={({ isActive }) =>
                    `px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                      isActive
                        ? 'bg-white text-teal-700 shadow-sm font-semibold'
                        : 'text-slate-600 hover:text-slate-900 hover:bg-white/40'
                    }`
                  }
                >
                  Query Logs
                </NavLink>
              </nav>
            </div>
          </div>
        </header>

        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/history" element={<History />} />
            <Route path="/history/:id" element={<History />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;