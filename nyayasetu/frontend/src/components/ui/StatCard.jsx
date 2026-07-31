import React from 'react';

/**
 * Reusable statistic counter card.
 * Replaces repeated stat card markup in CitizenDashboard and OfficerDashboard.
 */
export const StatCard = ({ icon: Icon, label, value, accentColor = 'var(--primary-blue)', warning = false }) => (
  <div className="stat-card"
    style={{
      backgroundColor: 'var(--bg-white)',
      border: `1px solid ${warning ? 'rgba(239,68,68,0.3)' : 'var(--border-color)'}`,
      borderRadius: 'var(--radius-md)',
      boxShadow: 'var(--shadow-sm)',
      padding: 'var(--space-5)',
      display: 'flex',
      alignItems: 'center',
      gap: 'var(--space-4)',
      transition: 'box-shadow var(--transition-fast)',
    }}
    onMouseEnter={e => e.currentTarget.style.boxShadow = 'var(--shadow-md)'}
    onMouseLeave={e => e.currentTarget.style.boxShadow = 'var(--shadow-sm)'}
  >
    <div className="stat-card"
      aria-hidden="true"
      style={{
        width: 44,
        height: 44,
        borderRadius: 'var(--radius-md)',
        backgroundColor: `${accentColor}1a`,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: accentColor,
        flexShrink: 0,
      }}
    >
      {Icon && <Icon size={20} />}
    </div>
    <div className="stat-card">
      <p style={{
        fontSize: 'var(--font-size-2xl)',
        fontWeight: 'var(--font-weight-bold)',
        color: warning ? '#ef4444' : 'var(--text-dark)',
        margin: 0,
        lineHeight: 1,
      }}>
        {value ?? '—'}
      </p>
      <p style={{
        fontSize: 'var(--font-size-sm)',
        color: 'var(--text-muted)',
        margin: 'var(--space-1) 0 0',
        fontWeight: 'var(--font-weight-medium)',
      }}>
        {label}
      </p>
    </div>
  </div>
);

export default StatCard;
