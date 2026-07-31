import React, { createContext, useContext, useMemo } from 'react';
import { useTheme } from '../hooks/useTheme';

const ThemeContext = createContext(null);

export const ThemeProvider = ({ children }) => {
  const { theme, toggleTheme, isDark } = useTheme();

  const value = useMemo(() => ({ theme, toggleTheme, isDark }), [theme, toggleTheme, isDark]);

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useThemeContext = () => useContext(ThemeContext);

export default ThemeContext;
