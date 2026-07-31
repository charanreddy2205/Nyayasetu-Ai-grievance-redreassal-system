import React, { useId } from 'react';
import { Search, X } from 'lucide-react';

/**
 * Accessible debounced search input with clear button.
 */
export const SearchBar = ({ value, onChange, placeholder = 'Search...', label, style: extraStyle = {} }) => {
  const id = useId();

  return (
    <div style={{ position: 'relative', display: 'flex', alignItems: 'center', ...extraStyle }}>
      {label && (
        <label htmlFor={id} className="sr-only">{label}</label>
      )}
      <Search
        size={16}
        aria-hidden="true"
        style={{
          position: 'absolute',
          left: 12,
          color: 'var(--text-subtle)',
          pointerEvents: 'none',
        }}
      />
      <input
        id={id}
        type="search"
        role="searchbox"
        aria-label={label || placeholder}
        value={value}
        onChange={e => onChange(e.target.value)}
        placeholder={placeholder}
        style={{
          width: '100%',
          padding: '0.5rem 2.25rem 0.5rem 2.25rem',
          border: '1.5px solid var(--border-color)',
          borderRadius: 'var(--radius-sm)',
          fontSize: 'var(--font-size-sm)',
          backgroundColor: 'var(--bg-white)',
          color: 'var(--text-dark)',
          transition: 'border-color var(--transition-fast), box-shadow var(--transition-fast)',
        }}
      />
      {value && (
        <button
          type="button"
          aria-label="Clear search"
          onClick={() => onChange('')}
          style={{
            position: 'absolute',
            right: 8,
            background: 'none',
            border: 'none',
            cursor: 'pointer',
            color: 'var(--text-muted)',
            display: 'flex',
            padding: 4,
            borderRadius: 'var(--radius-xs)',
          }}
        >
          <X size={14} />
        </button>
      )}
    </div>
  );
};

export default SearchBar;
