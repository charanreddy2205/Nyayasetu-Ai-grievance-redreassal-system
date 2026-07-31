import React from 'react';
import { Spinner } from './Spinner';

const BASE = {
  display: 'inline-flex',
  alignItems: 'center',
  justifyContent: 'center',
  gap: '0.5rem',
  fontFamily: 'var(--font-sans)',
  fontWeight: 'var(--font-weight-semibold)',
  borderRadius: 'var(--radius-sm)',
  border: '1.5px solid transparent',
  cursor: 'pointer',
  transition: 'all var(--transition-fast)',
  textDecoration: 'none',
  whiteSpace: 'nowrap',
};

const SIZES = {
  sm: { padding: '0.375rem 0.875rem', fontSize: 'var(--font-size-sm)' },
  md: { padding: '0.55rem 1.25rem',  fontSize: 'var(--font-size-base)' },
  lg: { padding: '0.75rem 1.75rem',  fontSize: 'var(--font-size-lg)' },
};

const VARIANTS = {
  primary: {
    backgroundColor: 'var(--primary-blue)',
    color: '#fff',
    borderColor: 'var(--primary-blue)',
  },
  secondary: {
    backgroundColor: 'var(--bg-white)',
    color: 'var(--text-dark)',
    borderColor: 'var(--border-color)',
  },
  success: {
    backgroundColor: 'var(--green)',
    color: '#fff',
    borderColor: 'var(--green)',
  },
  danger: {
    backgroundColor: '#ef4444',
    color: '#fff',
    borderColor: '#ef4444',
  },
  ghost: {
    backgroundColor: 'transparent',
    color: 'var(--primary-blue-light)',
    borderColor: 'transparent',
  },
  saffron: {
    backgroundColor: 'var(--saffron)',
    color: '#fff',
    borderColor: 'var(--saffron)',
  },
};

/**
 * Reusable Button with loading state, variants, and sizes.
 */
export const Button = ({
  children,
  variant = 'primary',
  size = 'md',
  loading = false,
  disabled = false,
  type = 'button',
  onClick,
  className = '',
  style: extraStyle = {},
  ...rest
}) => {
  const variantStyle = VARIANTS[variant] || VARIANTS.primary;
  const sizeStyle = SIZES[size] || SIZES.md;

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled || loading}
      aria-disabled={disabled || loading}
      aria-busy={loading}
      className={className}
      style={{
        ...BASE,
        ...variantStyle,
        ...sizeStyle,
        opacity: (disabled || loading) ? 0.6 : 1,
        cursor: (disabled || loading) ? 'not-allowed' : 'pointer',
        ...extraStyle,
      }}
      {...rest}
    >
      {loading && <Spinner size={16} />}
      {children}
    </button>
  );
};

export default Button;
