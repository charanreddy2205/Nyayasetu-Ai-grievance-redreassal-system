import React from 'react';

/**
 * Standard card container with optional title and header action slot.
 */
export const Card = ({ children, title, headerAction, style: extraStyle = {}, className = '' }) => (
  <div
    className={className}
    style={{
      backgroundColor: 'var(--bg-white)',
      border: '1px solid var(--border-color)',
      borderRadius: 'var(--radius-md)',
      boxShadow: 'var(--shadow-sm)',
      overflow: 'hidden',
      ...extraStyle,
    }}
  >
    {(title || headerAction) && (
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: 'var(--space-4) var(--space-6)',
        borderBottom: '1px solid var(--border-color)',
      }}>
        {title && (
          <h3 style={{ margin: 0, fontSize: 'var(--font-size-lg)', color: 'var(--text-dark)', fontWeight: 'var(--font-weight-semibold)' }}>
            {title}
          </h3>
        )}
        {headerAction && <div>{headerAction}</div>}
      </div>
    )}
    <div style={{ padding: 'var(--space-6)' }}>
      {children}
    </div>
  </div>
);

export default Card;
