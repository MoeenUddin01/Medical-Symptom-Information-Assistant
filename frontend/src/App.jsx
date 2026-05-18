import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import History from './pages/History';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <nav className="bg-white shadow-sm border-b border-gray-200">
          <div className="max-w-3xl mx-auto px-4">
            <div className="flex items-center justify-between h-16">
              <h1 className="text-xl font-bold text-gray-900">MedAssist</h1>
              <div className="flex items-center gap-6">
                <Link
                  to="/"
                  className="text-gray-600 hover:text-gray-900 font-medium transition-colors"
                >
                  Analyse Symptoms
                </Link>
                <Link
                  to="/history"
                  className="text-gray-600 hover:text-gray-900 font-medium transition-colors"
                >
                  History
                </Link>
              </div>
            </div>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/history" element={<History />} />
          <Route path="/history/:id" element={<History />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;