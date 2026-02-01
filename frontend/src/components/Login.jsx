import React, { useState } from 'react';
import apiFetch, { getCookie } from '../api/client';

export default function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const ensureCsrf = async () => {
    // Fetch CSRF token from backend endpoint
    const res = await fetch('/api/csrf/', { credentials: 'include' });
    if (!res.ok) throw new Error('Failed to get CSRF token');
    const data = await res.json();
    return data.csrfToken;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const csrftoken = await ensureCsrf();
      const body = new URLSearchParams();
      body.append('username', username);
      body.append('password', password);

      const res = await fetch('/api-auth/login/', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrftoken || ''
        },
        body: body.toString()
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(`Login failed: ${res.status} ${text}`);
      }

      if (onLogin) onLogin();
    } catch (err) {
      setError(err.message || String(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h3>Login</h3>
      <form onSubmit={handleSubmit}>
        <div className="form-row">
          <div>
            <label>Username</label>
            <input className="input" value={username} onChange={e => setUsername(e.target.value)} required />
          </div>
          <div>
            <label>Password</label>
            <input className="input" type="password" value={password} onChange={e => setPassword(e.target.value)} required />
          </div>
        </div>
        {error && <div style={{ color: 'red', marginBottom: 8 }}>{error}</div>}
        <div style={{ display: 'flex', gap: 8 }}>
          <button className="button" type="submit" disabled={loading}>{loading ? 'Signing in...' : 'Sign in'}</button>
        </div>
      </form>
    </div>
  );
}
