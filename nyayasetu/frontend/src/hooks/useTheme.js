import { useState, useEffect, useCallback } from 'react';

const STORAGE_KEY = 'nyayasetu_theme';

/**
 * Manages light/dark theme by toggling data-theme on <html>.
 * Persists preference to localStorage.
 */
export const useTheme = () => {
  const [theme, setTheme] = useState(() => {
    try {
      return localStorage.getItem(STORAGE_KEY) || 'light';
    } catch {
      return 'light';
    }
  });

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    try {
      localStorage.setItem(STORAGE_KEY, theme);
    } catch { /* ignore */ }
  }, [theme]);

  const toggleTheme = useCallback(() => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  }, []);

  return { theme, toggleTheme, isDark: theme === 'dark' };
};

export default useTheme;
