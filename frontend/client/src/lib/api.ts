/** Same-origin requests use Vite's proxy locally and the reverse proxy in production. */
export const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/$/, '');
let unauthorizedHandler: (() => void) | undefined;
export function setUnauthorizedHandler(handler?: () => void) { unauthorizedHandler = handler; }
const authRoutes: Record<string, string> = {
  '/login': '/api/v1/auth/login', '/signup': '/api/v1/auth/signup',
  '/logout': '/api/v1/auth/logout', '/test_token': '/api/v1/auth/test-token',
  '/password-reset': '/api/v1/auth/password-reset',
  '/password-reset-confirm': '/api/v1/auth/password-reset-confirm',
};
export class ApiError extends Error {
  constructor(message: string, public status: number) { super(message); }
}
export async function apiFetch<T = unknown>(path: string, options: RequestInit = {}): Promise<T> {
  const headers = new Headers(options.headers);
  const token = localStorage.getItem('authToken');
  const publicAuth = ['/login', '/signup', '/password-reset', '/password-reset-confirm'].includes(path);
  if (token && !publicAuth) headers.set('Authorization', `Token ${token}`);
  if (options.body && !(options.body instanceof FormData)) headers.set('Content-Type', 'application/json');
  const response = await fetch(`${API_BASE_URL}${authRoutes[path] || path}`, {
    ...options, headers, signal: options.signal || AbortSignal.timeout(30000),
  });
  if (response.status === 204) return undefined as T;
  const data = await response.json().catch(() => null);
  if (!response.ok) {
    if (response.status === 401 && !publicAuth && path !== '/logout') unauthorizedHandler?.();
    const message = data?.error || data?.detail || (data ? Object.entries(data).map(([key, value]) => `${key}: ${value}`).join('; ') : `Request failed (${response.status})`);
    throw new ApiError(String(message), response.status);
  }
  if (data === null) throw new ApiError('The server returned an invalid response.', response.status);
  return data as T;
}
export const apiGet = <T = unknown>(path: string) => apiFetch<T>(path);
export const apiPost = <T = unknown>(path: string, body: unknown) => apiFetch<T>(path, {
  method: 'POST', body: body instanceof FormData ? body : JSON.stringify(body),
});
