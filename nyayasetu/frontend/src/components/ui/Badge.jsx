import React from 'react';

const STATUS_STYLES = {
  pending:                { bg: 'var(--status-pending-bg)',  text: 'var(--status-pending-text)',  border: 'var(--status-pending-border)',  label: 'Pending' },
  in_progress:            { bg: 'var(--status-progress-bg)', text: 'var(--status-progress-text)', border: 'var(--status-progress-border)', label: 'In Progress' },
  resolved:               { bg: 'var(--status-resolved-bg)', text: 'var(--status-resolved-text)', border: 'var(--status-resolved-border)', label: 'Resolved' },
  escalated:              { bg: 'var(--status-escalated-bg)',text: 'var(--status-escalated-text)',border: 'var(--status-escalated-border)',label: 'Escalated' },
  administrative_failure: { bg: 'var(--status-failure-bg)',  text: 'var(--status-failure-text)',  border: 'var(--status-failure-border)',  label: 'Admin Failure' },
};

const URGENCY_STYLES = {
  low:      { bg: 'var(--urgency-low-bg)',      text: 'var(--urgency-low-text)',      label: 'Low' },
  medium:   { bg: 'var(--urgency-medium-bg)',   text: 'var(--urgency-medium-text)',   label: 'Medium' },
  high:     { bg: 'var(--urgency-high-bg)',     text: 'var(--urgency-high-text)',     label: 'High' },
  critical: { bg: 'var(--urgency-critical-bg)', text: 'var(--urgency-critical-text)', label: 'Critical' },
};

/**
 * Unified Badge component for status and urgency values.
 * @param {'status'|'urgency'} variant
 * @param {string} value - e.g. 'pending', 'critical'
 * @param {string} [className]
 */
export const Badge = ({ variant = 'status', value = '', className = '' }) => {
  const map = variant === 'urgency' ? URGENCY_STYLES : STATUS_STYLES;
  const style = map[value] || { bg: 'var(--bg-subtle)', text: 'var(--text-muted)', label: value };

  return (
    <span
      role="status"
      aria-label={`${variant}: ${style.label}`}
      className={className}
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        padding: '2px 10px',
        borderRadius: 'var(--radius-full)',
        fontSize: 'var(--font-size-xs)',
        fontWeight: 'var(--font-weight-semibold)',
        letterSpacing: '0.03em',
        textTransform: 'uppercase',
        whiteSpace: 'nowrap',
        backgroundColor: style.bg,
        color: style.text,
        border: style.border ? `1px solid ${style.border}` : 'none',
      }}
    >
      {style.label}
    </span>
  );
};

export default Badge;
