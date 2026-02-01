import React, { useEffect, useState } from 'react';
import apiFetch from '../api/client';

export default function WorkoutList({ refreshKey = 0 }) {
  const [data, setData] = useState({ count: 0, next: null, previous: null, results: [] });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchUrl = async (urlPath = '/workouts/') => {
    try {
      setLoading(true);
      setError(null);
      const d = await apiFetch(urlPath);
      setData(d);
    } catch (err) {
      setError(err.message || String(err));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchUrl('/workouts/'); }, [refreshKey]);

  if (loading) return <div className="card">Loading workouts...</div>;
  if (error) return <div className="card">Error: {error}</div>;

  const rows = Array.isArray(data && data.results) ? data.results : [];

  return (
    <div className="card">
      <h3>Workouts ({data.count})</h3>
      <table className="table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Type</th>
            <th>Distance (km)</th>
            <th>Duration (min)</th>
            <th>Calories</th>
            <th>Notes</th>
          </tr>
        </thead>
        <tbody>
          {rows.map(w => (
            <tr key={w.id}>
              <td>{w.date}</td>
              <td>{w.workout_type_display}</td>
              <td>{w.distance ? w.distance.toFixed(2) : ''}</td>
              <td>{w.duration}</td>
              <td>{w.calories}</td>
              <td>{w.notes || ''}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <div style={{ marginTop: 12, display: 'flex', gap: 8 }}>
        <button className="button secondary" disabled={!data.previous} onClick={() => fetchUrl(data.previous || '/workouts/')}>Previous</button>
        <button className="button" disabled={!data.next} onClick={() => fetchUrl(data.next || '/workouts/')}>Next</button>
      </div>
    </div>
  );
}
