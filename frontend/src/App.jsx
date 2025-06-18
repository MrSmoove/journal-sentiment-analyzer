import { useState, useEffect } from 'react';
import './App.css';

const STORAGE_KEY = 'journal_entries';
const MAX_ENTRIES = 5000; // character limit
const RATE_LIMIT_MS = 10000; // 10 seconds

const moodMap = {
  POSITIVE: { emoji: '✨', color: '#d4a574' },
  NEGATIVE: { emoji: '🍂', color: '#8b4513' },
  NEUTRAL: { emoji: '🌱', color: '#9c7a5b' },
  MIXED: { emoji: '🌿', color: '#b8855f' },
};

function App() {
  const [entry, setEntry] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState([]);
  const [lastSubmission, setLastSubmission] = useState(0);

  // Load saved entries
  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      setHistory(JSON.parse(saved));
    }
  }, []);

  const saveToHistory = (entryData) => {
    const updated = [
      { ...entryData, timestamp: new Date().toISOString() },
      ...history,
    ].slice(0, 10); // latest 10 only

    setHistory(updated);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
  };

  const handleInputChange = (e) => {
    const value = e.target.value;
    if (value.length <= MAX_ENTRIES) {
      setEntry(value);
      setError(null);
    } else {
      setError(`Max ${MAX_ENTRIES} characters.`);
    }
  };

  const analyzeEntry = async () => {
    if (!entry.trim()) {
      setError('Please write something first.');
      return;
    }

    const now = Date.now();
    if (now - lastSubmission < RATE_LIMIT_MS) {
      setError(`Wait ${Math.ceil((RATE_LIMIT_MS - (now - lastSubmission)) / 1000)}s before submitting again.`);
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(import.meta.env.VITE_API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: entry })
      });

      if (!response.ok) throw new Error('Something went wrong with analysis.');

      const data = await response.json();
      setResult(data);
      saveToHistory({ entry, ...data });
      setLastSubmission(Date.now());
    } catch (err) {
      setError(err.message);
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="soul-container">
      <div className="warm-card">
        <h1 className="soul-title">Soul Journal</h1>

        {error && <div className="error-message">{error}</div>}

        <textarea
          className="earth-input"
          value={entry}
          onChange={handleInputChange}
          rows={6}
          placeholder="Share your thoughts, let them flow..."
          disabled={loading}
        />

        <div className="char-count">{entry.length}/{MAX_ENTRIES}</div>

        <button
          className="soul-button"
          onClick={analyzeEntry}
          disabled={loading || !entry.trim()}
        >
          {loading ? 'Finding your rhythm...' : 'Reflect on These Words'}
        </button>

        {result && (
          <div className="result-soul animate-fade-in">
            <h2 className="sentiment-heading" style={{ color: moodMap[result.sentiment]?.color }}>
              <span className="mood-emoji">{moodMap[result.sentiment]?.emoji}</span>
              {result.sentiment.toLowerCase()}
            </h2>
            <p className="analysis-text">{result.summary}</p>
            <p className="analysis-text">{result.prompt}</p>
            <div className="key-phrases">
              {result.key_phrases?.map((phrase, idx) => (
                <span key={idx} className="phrase-tag">{phrase}</span>
              ))}
            </div>
          </div>
        )}

        {history.length > 0 && (
          <div className="history-section">
            <h3>Previous Entries</h3>
            {history.map((item, idx) => (
              <div key={idx} className="history-item">
                <span className="history-date">
                  {new Date(item.timestamp).toLocaleDateString()}
                </span>
                <span className="history-mood">{moodMap[item.sentiment]?.emoji}</span>
                <p className="history-text">{item.entry.slice(0, 50)}...</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
