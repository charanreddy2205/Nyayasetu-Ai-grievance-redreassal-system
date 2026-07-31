import React from 'react';

/**
 * Accessible spinner with role="status" and sr-only label.
 */
export const Spinner = ({ size = 20, color = 'currentColor', label = 'Loading...' }) => (
  <span role="status" aria-label={label} style={{ display: 'inline-flex', alignItems: 'center' }}>
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke={color}
      strokeWidth="2.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      style={{ animation: 'spin 0.75s linear infinite' }}
    >
      <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83" />
    </svg>
    <span className="sr-only">{label}</span>
  </span>
);

export default Spinner;
