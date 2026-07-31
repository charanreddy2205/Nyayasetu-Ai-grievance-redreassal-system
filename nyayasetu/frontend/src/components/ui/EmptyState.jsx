import React from 'react';
import { FileText } from 'lucide-react';
import { Button } from './Button';

/**
 * Generic empty state with icon, heading, description, and optional action.
 */
export const EmptyState = ({
  icon: Icon = FileText,
  title = 'Nothing here yet',
  description = '',
  action,
  actionLabel,
  onAction,
}) => (
  <div
    role="status"
    aria-live="polite"
    style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      padding: 'var(--space-16) var(--space-8)',
      textAlign: 'center',
      gap: 'var(--space-4)',
    }}
  >
    <div
      aria-hidden="true"
      style={{
        width: 64,
        height: 64,
        borderRadius: 'var(--radius-full)',
        backgroundColor: 'var(--bg-subtle)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: 'var(--text-subtle)',
      }}
    >
      <Icon size={28} />
    </div>

    <div>
      <h4 style={{ margin: 0, color: 'var(--text-dark)', fontSize: 'var(--font-size-lg)' }}>
        {title}
      </h4>
      {description && (
        <p style={{ margin: 'var(--space-2) 0 0', color: 'var(--text-muted)', fontSize: 'var(--font-size-sm)' }}>
          {description}
        </p>
      )}
    </div>

    {(action || onAction) && actionLabel && (
      <Button variant="primary" size="sm" onClick={onAction}>
        {action || actionLabel}
      </Button>
    )}
  </div>
);

export default EmptyState;
