import { useState, useEffect, useCallback, useRef } from 'react';
import { useAuth } from '../context/AuthContext';

/**
 * Generic data-fetching hook using the authenticated apiFetch.
 *
 * @param {string|null} url - API endpoint. Pass null to skip fetching.
 * @param {object} options - fetch options
 * @returns {{ data, loading, error, refetch }}
 */
export const useApi = (url, options = {}) => {
  const { apiFetch } = useAuth();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(!!url);
  const [error, setError] = useState(null);
  // Stable ref so we can cancel stale fetches
  const abortRef = useRef(null);

  const fetchData = useCallback(async (silent = false) => {
    if (!url) return;
    if (!silent) setLoading(true);
    setError(null);

    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;

    try {
      const res = await apiFetch(url, { ...options, signal: controller.signal });
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}: ${res.statusText}`);
      }
      const json = await res.json();
      setData(json);
    } catch (err) {
      if (err.name !== 'AbortError') {
        setError(err.message || 'An error occurred');
      }
    } finally {
      if (!controller.signal.aborted) {
        setLoading(false);
      }
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [url]);

  useEffect(() => {
    fetchData();
    return () => abortRef.current?.abort();
  }, [fetchData]);

  const refetch = useCallback((silent = false) => fetchData(silent), [fetchData]);

  return { data, loading, error, refetch };
};

export default useApi;
