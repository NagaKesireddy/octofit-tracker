// Read API base from environment at build time; fall back to relative '/api'
export const API_BASE = process.env.REACT_APP_API_BASE || '/api';

export default async function apiFetch(path, options = {}) {
  // allow passing absolute URLs (for next/previous links) or relative paths
  const isAbsolute = typeof path === 'string' && (path.startsWith('http://') || path.startsWith('https://') || path.startsWith('//'));
  const url = isAbsolute ? path : (API_BASE + path);
  const opts = Object.assign({
    headers: { 'Content-Type': 'application/json' },
    // include cookies for session authentication when available
    credentials: 'include'
  }, options);

  // If this is a mutating request, attach CSRF header from cookie when present
  const method = (opts.method || 'GET').toUpperCase();
  const safeMethods = ['GET', 'HEAD', 'OPTIONS', 'TRACE'];
  if (!safeMethods.includes(method)) {
    let csrf = getCookie('csrftoken');
    // If cookie is not available (proxy/origin differences), try fetching token from backend endpoint
    if (!csrf) {
      try {
        const tokenRes = await fetch(API_BASE + '/csrf/', { credentials: 'include' });
        if (tokenRes.ok) {
          const data = await tokenRes.json();
          csrf = data && data.csrfToken;
        }
      } catch (e) {
        // ignore; we'll proceed without token and let server respond with proper error
      }
    }

    if (csrf && !opts.headers['X-CSRFToken'] && !opts.headers['x-csrftoken']) {
      opts.headers['X-CSRFToken'] = csrf;
    }
  }

  const res = await fetch(url, opts);
  if (!res.ok) {
    const text = await res.text();
    const err = new Error(`HTTP ${res.status}: ${text}`);
    err.status = res.status;
    throw err;
  }
  const contentType = res.headers.get('content-type') || '';
  if (contentType.includes('application/json')) return res.json();
  return res.text();
}

export function getCookie(name) {
  if (typeof document === 'undefined') return null;
  const matches = document.cookie.match(new RegExp('(?:^|; )' + name.replace(/([.$?*|{}()[]\\\/\\+^])/g, '\\$1') + '=([^;]*)'));
  return matches ? decodeURIComponent(matches[1]) : null;
}
