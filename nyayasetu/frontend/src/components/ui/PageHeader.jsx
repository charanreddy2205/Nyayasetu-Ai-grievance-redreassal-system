import React from 'react';

/**
 * Reusable page header with title, subtitle, and right-side action slot.
 */
export const PageHeader = ({ title, subtitle, action, icon: Icon }) => (
  <div style={{
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    flexWrap: 'wrap',
    gap: 'var(--space-4)',
    marginBottom: 'var(--space-6)',
  }}>
    <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)' }}>
      {Icon && (
        <div aria-hidden="true" style={{
          width: 42,
          height: 42,
          borderRadius: 'var(--radius-md)',
          backgroundColor: 'var(--primary-blue)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: '#fff',
        }}>
          <Icon size={20} />
        </div>
      )}
      <div>
        <h1 style={{ margin: 0, fontSize: 'var(--font-size-2xl)', color: 'var(--text-dark)', fontWeight: 'var(--font-weight-bold)' }}>
          {title}
        </h1>
        {subtitle && (
          <p style={{ margin: 0, fontSize: 'var(--font-size-sm)', color: 'var(--text-muted)', marginTop: 'var(--space-1)' }}>
            {subtitle}
          </p>
        )}
      </div>
    </div>
    {action && <div>{action}</div>}
  </div>
);

export default PageHeader;
