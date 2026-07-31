import React, { createContext, useState, useEffect, useContext, useMemo, useCallback } from 'react';

const AuthStateContext = createContext(null);
const AuthActionsContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [csrfToken, setCsrfToken] = useState('');

  /** Fetch session status + refresh CSRF token */
  const checkSession = useCallback(async () => {
    try {
      const response = await fetch('/api/auth/session/', {
        method: 'GET',
        headers: { Accept: 'application/json' },
      });
      const data = await response.json();
      const normalizedUser = data?.user || data?.data?.user || {
        username: data?.username,
        firstName: data?.firstName,
        lastName: data?.lastName,
        email: data?.email,
        role: data?.role,
        department: data?.department,
      };

      if (data?.isAuthenticated || data?.success) {
        setUser(normalizedUser && Object.keys(normalizedUser).length > 0 ? normalizedUser : null);
      } else {
        setUser(null);
      }
      if (data?.csrfToken) setCsrfToken(data.csrfToken);
    } catch {
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { checkSession(); }, [checkSession]);

  const login = useCallback(async (username, password) => {
    try {
      const response = await fetch('/api/auth/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
        body: JSON.stringify({ username, password }),
      });
      const data = await response.json();
      const normalizedUser = data?.user || data?.data?.user || null;
      if (response.ok && (data.success || data.isAuthenticated || normalizedUser)) {
        setUser(normalizedUser);
        await checkSession();
        return { success: true };
      }
      return { success: false, error: data.error || data.message || 'Login failed' };
    } catch {
      return { success: false, error: 'Network error occurred' };
    }
  }, [csrfToken, checkSession]);

  const register = useCallback(async (username, firstName, lastName, email, password) => {
    try {
      const response = await fetch('/api/auth/register/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
        body: JSON.stringify({ username, firstName, lastName, email, password }),
      });
      const data = await response.json();
      const normalizedUser = data?.user || data?.data?.user || null;
      if (response.ok && (data.success || normalizedUser)) {
        setUser(normalizedUser);
        await checkSession();
        return { success: true };
      }
      return { success: false, error: data.error || data.message || 'Registration failed' };
    } catch {
      return { success: false, error: 'Network error occurred' };
    }
  }, [csrfToken, checkSession]);

  const logout = useCallback(async () => {
    try {
      await fetch('/api/auth/logout/', {
        method: 'POST',
        headers: { 'X-CSRFToken': csrfToken },
      });
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      setUser(null);
      setCsrfToken('');
    }
    return { success: true };
  }, [csrfToken]);

  /**
   * Authenticated API helper — automatically includes CSRF and handles 401.
   * Does NOT set Content-Type for FormData (multipart uploads).
   */
  const apiFetch = useCallback(async (url, options = {}) => {
    const headers = { ...options.headers };
    headers['X-CSRFToken'] = csrfToken;
    if (!(options.body instanceof FormData)) {
      headers['Content-Type'] = headers['Content-Type'] || 'application/json';
    }

    const response = await fetch(url, { ...options, headers });

    if (response.status === 401 || response.status === 403) {
      const sessionRes = await fetch('/api/auth/session/');
      const sessionData = await sessionRes.json();
      if (!sessionData.isAuthenticated) setUser(null);
    }

    return response;
  }, [csrfToken]);

  const stateValue = useMemo(() => ({
    user,
    loading,
    csrfToken,
  }), [user, loading, csrfToken]);

  const actionsValue = useMemo(() => ({
    login,
    register,
    logout,
    apiFetch,
    checkSession,
  }), [login, register, logout, apiFetch, checkSession]);

  return (
    <AuthStateContext.Provider value={stateValue}>
      <AuthActionsContext.Provider value={actionsValue}>
        {children}
      </AuthActionsContext.Provider>
    </AuthStateContext.Provider>
  );
};

/** Full auth context for legacy compatibility (combines state and actions) */
export const useAuth = () => {
  const state = useContext(AuthStateContext);
  const actions = useContext(AuthActionsContext);
  return { ...state, ...actions };
};

/** Lightweight hook — only subscribes to user object */
export const useUser = () => {
  const { user } = useContext(AuthStateContext);
  return user;
};

/** Hook for the authenticated fetch utility only (no re-renders on user state change) */
export const useApiFetch = () => {
  const { apiFetch } = useContext(AuthActionsContext);
  return apiFetch;
};

export default AuthStateContext;
