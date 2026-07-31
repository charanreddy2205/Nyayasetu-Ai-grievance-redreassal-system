import { useState, useEffect } from 'react';

/**
 * Delays updating a value until the user stops typing.
 * @param {*} value - The value to debounce
 * @param {number} delay - Delay in ms (default 350)
 * @returns debounced value
 */
export const useDebounce = (value, delay = 350) => {
  const [debounced, setDebounced] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debounced;
};

export default useDebounce;
