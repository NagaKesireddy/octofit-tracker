import React, { useState } from 'react';
import apiFetch from '../api/client';

const TYPES = [
  { value: 'run', label: 'Running' },
  { value: 'walk', label: 'Walking' },
  { value: 'cycling', label: 'Cycling' },
  { value: 'gym', label: 'Gym' }
];

export default function WorkoutForm({ onWorkoutCreated }) {
  const [date, setDate] = useState('');
  const [workoutType, setWorkoutType] = useState('run');
  const [duration, setDuration] = useState('');
  const [distance, setDistance] = useState('');
  const [calories, setCalories] = useState('');
  const [notes, setNotes] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const reset = () => { setDate(''); setWorkoutType('run'); setDuration(''); setDistance(''); setCalories(''); setNotes(''); };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const payload = {
        date,
        workout_type: workoutType,
        duration: duration ? Number(duration) : 0,
        distance: distance ? Number(distance) : 0,
        calories: calories ? Number(calories) : 0,
        notes: notes || null
      };

      await apiFetch('/workouts/', {
        method: 'POST',
        body: JSON.stringify(payload)
      });

      reset();
      if (onWorkoutCreated) onWorkoutCreated();
    } catch (err) {
      setError(err.message || String(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h3>Create Workout</h3>
      <form onSubmit={handleSubmit}>
        <div className="form-row">
          <div>
            <label>Date</label>
            <input className="input" type="date" value={date} onChange={e => setDate(e.target.value)} required />
          </div>
          <div>
            <label>Type</label>
            <select className="input" value={workoutType} onChange={e => setWorkoutType(e.target.value)}>
              {TYPES.map(t => <option key={t.value} value={t.value}>{t.label}</option>)}
            </select>
          </div>
        </div>

        <div className="form-row">
          <div>
            <label>Duration (minutes)</label>
            <input className="input" type="number" min="0" value={duration} onChange={e => setDuration(e.target.value)} required />
          </div>
          <div>
            <label>Distance (km)</label>
            <input className="input" type="number" step="0.01" min="0" value={distance} onChange={e => setDistance(e.target.value)} />
          </div>
        </div>

        <div className="form-row">
          <div>
            <label>Calories</label>
            <input className="input" type="number" min="0" value={calories} onChange={e => setCalories(e.target.value)} />
          </div>
        </div>

        <div className="form-row single">
          <div>
            <label>Notes</label>
            <textarea className="input" rows="3" value={notes} onChange={e => setNotes(e.target.value)} />
          </div>
        </div>

        {error && <div style={{ color: 'red', marginBottom: 8 }}>{error}</div>}
        <div style={{ display: 'flex', gap: 8 }}>
          <button className="button" type="submit" disabled={loading}>{loading ? 'Saving...' : 'Create'}</button>
        </div>
      </form>
    </div>
  );
}
