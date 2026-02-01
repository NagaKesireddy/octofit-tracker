import React, { useState } from 'react';
import WorkoutForm from '../components/WorkoutForm';
import WorkoutList from '../components/WorkoutList';
import Login from '../components/Login';

export default function Dashboard() {
  const [refreshKey, setRefreshKey] = useState(0);
  const handleCreated = () => setRefreshKey(k => k + 1);
  const handleLogin = () => setRefreshKey(k => k + 1);

  return (
    <div className="container">
      <h1>OctoFit Dashboard</h1>
      <Login onLogin={handleLogin} />
      <WorkoutForm onWorkoutCreated={handleCreated} />
      <WorkoutList refreshKey={refreshKey} />
    </div>
  );
}
