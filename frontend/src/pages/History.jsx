import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import SeverityBadge from '../components/SeverityBadge';

function History() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [queries, setQueries] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // Detail query states
  const [selectedQuery, setSelectedQuery] = useState(null);
  const [isDetailLoading, setIsDetailLoading] = useState(false);
  const [detailError, setDetailError] = useState(null);

  useEffect(() => {
    fetchHistory();
  }, []);

  useEffect(() => {
    if (id) {
      fetchQueryDetail(id);
    } else {
      setSelectedQuery(null);
    }
  }, [id]);

  const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

  const fetchHistory = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch(`${BACKEND_URL}/api/history`);
      if (!response.ok) {
        throw new Error('Failed to fetch queries list.');
      }
      const data = await response.json();
      setQueries(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchQueryDetail = async (queryId) => {
    setIsDetailLoading(true);
    setDetailError(null);
    try {
      const response = await fetch(`${BACKEND_URL}/api/history/${queryId}`);
      if (!response.ok) {
        throw new Error('Failed to fetch detailed clinical log.');
      }
      const data = await response.json();
      setSelectedQuery(data);
    } catch (err) {
      setDetailError(err.message);
    } finally {
      setIsDetailLoading(false);
    }
  };

  const formatFullDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  const truncateText = (text, maxLength = 80) => {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-slate-50/20 py-8 px-6">
        <div className="max-w-3xl mx-auto space-y-4">
          <div className="bg-slate-200 h-8 w-48 rounded-xl animate-pulse"></div>
          {[1, 2, 3].map((i) => (
            <div key={i} className="bg-slate-100 h-24 rounded-2xl animate-pulse"></div>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-slate-50/20 py-8 px-6">
        <div className="max-w-3xl mx-auto">
          <div className="bg-red-50 border border-red-200 rounded-2xl p-5 text-red-700 premium-glow">
            <h3 className="font-bold font-outfit text-sm">Failed to load logs</h3>
            <p className="text-xs mt-1 leading-normal">{error}</p>
            <button
              onClick={fetchHistory}
              className="mt-3 px-4 py-2 bg-red-600 text-white rounded-xl text-xs font-bold hover:bg-red-700 transition-colors"
            >
              Retry Connection
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50/20 py-8 px-6">
      <div className="max-w-3xl mx-auto space-y-6">
        
        {/* Title Bar */}
        <div className="flex items-center justify-between px-2">
          <div className="space-y-0.5">
            <h2 className="text-2xl font-extrabold text-slate-800 font-outfit tracking-tight">Recent Diagnoses</h2>
            <p className="text-slate-500 text-xs font-medium">Logs of clinical queries evaluated by the assistant.</p>
          </div>
          <button 
            onClick={fetchHistory}
            className="p-2 rounded-xl border border-slate-200 bg-white hover:bg-slate-50 transition-colors text-slate-600 hover:text-slate-900"
            title="Refresh logs"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
            </svg>
          </button>
        </div>

        {/* List of queries */}
        {queries.length === 0 ? (
          <div className="bg-white border border-slate-100 rounded-3xl p-12 text-center premium-glow">
            <svg className="w-16 h-16 text-slate-200 mx-auto mb-4" fill="none" stroke="currentColor" strokeWidth="1.5" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 12h16.5m-16.5 3.75h16.5M3.75 19.5h16.5M5.625 4.5h12.75a1.875 1.875 0 010 3.75H5.625a1.875 1.875 0 010-3.75z" />
            </svg>
            <h3 className="text-sm font-bold text-slate-700 tracking-wide">No diagnostic logs recorded</h3>
            <p className="text-xs text-slate-500 mt-1 max-w-xs mx-auto leading-normal">
              You haven't checked any symptoms yet. Go back to the homepage to run a symptom check!
            </p>
          </div>
        ) : (
          <div className="grid gap-3.5">
            {queries.map((query) => (
              <div
                key={query.id}
                className="bg-white border border-slate-100/90 rounded-2xl shadow-sm hover:shadow-md p-5 flex flex-col md:flex-row md:items-center justify-between gap-4 transition-all duration-300 premium-glow"
              >
                <div className="flex-1 min-w-0 space-y-2">
                  <p className="text-slate-800 font-bold text-sm leading-snug font-sans tracking-tight">
                    "{truncateText(query.symptom_text)}"
                  </p>
                  <div className="flex flex-wrap items-center gap-3">
                    <span
                      className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold border ${
                        query.is_emergency
                          ? 'bg-rose-50 text-rose-700 border-rose-100'
                          : 'bg-emerald-50 text-emerald-700 border-emerald-100'
                      }`}
                    >
                      <span className={`w-1.5 h-1.5 rounded-full ${query.is_emergency ? 'bg-rose-500' : 'bg-emerald-500'}`} />
                      {query.is_emergency ? 'Emergency' : 'Evaluated'}
                    </span>
                    <span className="text-[11px] font-semibold text-slate-500 bg-slate-100 px-2 py-0.5 rounded-md">
                      {query.conditions_count} matched condition{query.conditions_count !== 1 ? 's' : ''}
                    </span>
                    <span className="text-[10px] font-medium text-slate-400">
                      {new Date(query.created_at).toLocaleDateString()}
                    </span>
                  </div>
                </div>
                <button
                  onClick={() => navigate(`/history/${query.id}`)}
                  className="w-full md:w-auto px-4 py-2.5 bg-slate-50 hover:bg-teal-50 hover:text-teal-700 text-slate-700 text-xs font-bold rounded-xl border border-slate-200/60 hover:border-teal-200 transition-all duration-300 text-center flex-shrink-0 active:scale-[0.98]"
                >
                  View Dossier
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Case Dossier Slide-Over Modal Overlay */}
      {(id || isDetailLoading) && (
        <div className="fixed inset-0 z-50 overflow-hidden bg-slate-900/40 backdrop-blur-sm flex items-center justify-end">
          {/* Backdrop Closer */}
          <div className="absolute inset-0 cursor-default" onClick={() => navigate('/history')}></div>
          
          <div className="relative w-full max-w-lg h-full bg-white shadow-2xl flex flex-col z-10 animate-slide-in overflow-hidden border-l border-slate-100">
            {/* Header */}
            <div className="p-6 border-b border-slate-100 flex items-center justify-between bg-slate-50/50">
              <div className="space-y-0.5">
                <span className="text-[10px] font-extrabold text-teal-600 tracking-wider uppercase font-outfit">Clinical Audit File</span>
                <h3 className="text-lg font-extrabold text-slate-900 font-outfit">Health Case Dossier</h3>
              </div>
              <button
                onClick={() => navigate('/history')}
                className="p-2 rounded-xl hover:bg-slate-100 transition-colors text-slate-500 hover:text-slate-900"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {/* Dossier Content Body */}
            <div className="flex-1 overflow-y-auto p-6 space-y-6">
              {isDetailLoading ? (
                <div className="flex flex-col items-center justify-center h-64 space-y-4">
                  <svg className="animate-spin h-8 w-8 text-teal-600" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <p className="text-slate-500 text-xs font-bold tracking-wide animate-pulse">Retrieving Clinical Dossier File...</p>
                </div>
              ) : detailError ? (
                <div className="bg-red-50 border border-red-200 rounded-2xl p-5 text-center space-y-2">
                  <p className="text-sm font-bold text-red-800">Dossier Load Failure</p>
                  <p className="text-xs text-red-700">{detailError}</p>
                </div>
              ) : selectedQuery ? (
                <div className="space-y-6">
                  {/* Metadata Row */}
                  <div className="bg-slate-50/80 rounded-2xl p-4 border border-slate-100 text-xs space-y-2 text-slate-500 font-semibold select-none">
                    <div className="flex justify-between">
                      <span>Dossier ID:</span>
                      <span className="font-mono text-[10px] text-slate-700">{selectedQuery.id}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Evaluation Date:</span>
                      <span className="text-slate-700">{formatFullDate(selectedQuery.created_at)}</span>
                    </div>
                  </div>

                  {/* Symptom Text transcript */}
                  <div className="space-y-2">
                    <h4 className="text-xs font-bold text-slate-500 tracking-wider uppercase font-outfit">Symptom Case Report</h4>
                    <div className="bg-slate-50 border border-slate-200/50 rounded-2xl p-4 font-sans text-sm italic text-slate-700 leading-relaxed tracking-tight shadow-inner">
                      "{selectedQuery.symptom_text}"
                    </div>
                  </div>

                  {/* Evaluation Status Banner */}
                  <div className="space-y-2">
                    <h4 className="text-xs font-bold text-slate-500 tracking-wider uppercase font-outfit">Emergency Triage</h4>
                    {selectedQuery.is_emergency ? (
                      <div className="bg-rose-50 border border-rose-200 rounded-2xl p-4 flex items-center gap-3">
                        <span className="flex h-3.5 w-3.5 relative flex-shrink-0">
                          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
                          <span className="relative inline-flex rounded-full h-3.5 w-3.5 bg-rose-500"></span>
                        </span>
                        <div>
                          <p className="text-sm font-bold text-rose-800">High Risk Condition Indicated</p>
                          <p className="text-xs text-rose-700 mt-0.5 leading-normal">
                            This patient query was triaged as an emergency matching critical safety keywords (such as: {selectedQuery.matched_keyword || 'general emergency'}).
                          </p>
                        </div>
                      </div>
                    ) : (
                      <div className="bg-emerald-50 border border-emerald-100 rounded-2xl p-4 flex items-center gap-3">
                        <span className="w-3.5 h-3.5 rounded-full bg-emerald-500 flex-shrink-0" />
                        <div>
                          <p className="text-sm font-bold text-emerald-800">Normal Triage Evaluation</p>
                          <p className="text-xs text-emerald-700 mt-0.5 leading-normal">
                            No immediate high-risk clinical safety keywords were matching in the symptom transcript.
                          </p>
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Conditions List */}
                  <div className="space-y-4">
                    <h4 className="text-xs font-bold text-slate-500 tracking-wider uppercase font-outfit">
                      Identified Reference Pathology Chunks ({selectedQuery.conditions_count})
                    </h4>
                    {selectedQuery.conditions && selectedQuery.conditions.length > 0 ? (
                      <div className="space-y-3.5">
                        {selectedQuery.conditions.map((condition, idx) => {
                          const severityBorder = {
                            mild: 'border-emerald-200 bg-emerald-50/20 text-emerald-800',
                            moderate: 'border-amber-200 bg-amber-50/20 text-amber-800',
                            urgent: 'border-rose-200 bg-rose-50/20 text-rose-800'
                          }[condition.severity] || 'border-slate-200 bg-slate-50';

                          return (
                            <div key={idx} className={`p-4 border rounded-2xl space-y-2.5 ${severityBorder}`}>
                              <div className="flex items-center justify-between gap-4">
                                <h5 className="font-bold text-slate-800 text-sm font-outfit tracking-tight">{condition.name}</h5>
                                <SeverityBadge severity={condition.severity} />
                              </div>
                              <p className="text-xs text-slate-600 leading-relaxed font-medium">{condition.explanation}</p>
                              <div className="text-[10px] font-semibold text-slate-400 flex items-center gap-1">
                                <svg className="w-3 h-3 text-slate-400" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
                                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747" />
                                </svg>
                                Verified Source: {condition.source}
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    ) : (
                      <div className="bg-slate-50 border border-slate-200/50 rounded-2xl p-6 text-center select-none">
                        <p className="text-xs font-semibold text-slate-500">No matching medical reference segments found for this log.</p>
                      </div>
                    )}
                  </div>
                </div>
              ) : null}
            </div>

            {/* Footer Closer */}
            <div className="p-5 border-t border-slate-100 bg-slate-50/30">
              <button
                onClick={() => navigate('/history')}
                className="w-full py-3 bg-slate-800 text-white rounded-xl text-xs font-bold hover:bg-slate-900 transition-colors shadow-md text-center"
              >
                Close Audit File
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default History;