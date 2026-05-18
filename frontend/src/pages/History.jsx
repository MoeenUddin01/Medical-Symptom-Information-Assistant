import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';

function History() {
  const [queries, setQueries] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:8000/api/history');
      if (!response.ok) {
        throw new Error('Failed to fetch history');
      }
      const data = await response.json();
      setQueries(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const formatTimeAgo = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const seconds = Math.floor((now - date) / 1000);

    if (seconds < 60) return 'just now';
    const minutes = Math.floor(seconds / 60);
    if (minutes < 60) return `${minutes} minute${minutes !== 1 ? 's' : ''} ago`;
    const hours = Math.floor(minutes / 60);
    if (hours < 24) return `${hours} hour${hours !== 1 ? 's' : ''} ago`;
    const days = Math.floor(hours / 24);
    if (days < 30) return `${days} day${days !== 1 ? 's' : ''} ago`;
    const months = Math.floor(days / 30);
    return `${months} month${months !== 1 ? 's' : ''} ago`;
  };

  const truncateText = (text, maxLength = 100) => {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8 px-4">
        <div className="max-w-3xl mx-auto space-y-4">
          <div className="bg-gray-200 h-8 w-48 rounded animate-pulse"></div>
          {[1, 2, 3].map((i) => (
            <div key={i} className="bg-gray-200 h-24 rounded animate-pulse"></div>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 py-8 px-4">
        <div className="max-w-3xl mx-auto">
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
            <p className="font-medium">Failed to load history</p>
            <p className="text-sm mt-1">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-3xl mx-auto space-y-4">
        <h2 className="text-xl font-semibold text-gray-900">Recent Searches</h2>

        {queries.length === 0 ? (
          <div className="bg-gray-100 rounded-lg p-6 text-center">
            <p className="text-gray-500">No searches yet. Start by analyzing your symptoms!</p>
          </div>
        ) : (
          queries.map((query) => (
            <div
              key={query.id}
              className="bg-white border border-gray-200 rounded-lg shadow-sm p-4 flex items-center justify-between"
            >
              <div className="flex-1 min-w-0 mr-4">
                <p className="text-gray-900 font-medium truncate">
                  {truncateText(query.symptom_text)}
                </p>
                <div className="flex items-center gap-3 mt-2">
                  <span
                    className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
                      query.is_emergency
                        ? 'bg-red-100 text-red-700'
                        : 'bg-green-100 text-green-700'
                    }`}
                  >
                    {query.is_emergency ? 'Emergency' : 'Normal'}
                  </span>
                  <span className="text-sm text-gray-500">
                    {query.conditions_count} condition{query.conditions_count !== 1 ? 's' : ''}
                  </span>
                  <span className="text-sm text-gray-400">
                    {formatTimeAgo(query.created_at)}
                  </span>
                </div>
              </div>
              <Link
                to={`/history/${query.id}`}
                className="flex-shrink-0 px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors"
              >
                View Details
              </Link>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

History.propTypes = {};

export default History;