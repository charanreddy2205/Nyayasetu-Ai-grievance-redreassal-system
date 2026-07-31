import { useState, useCallback } from 'react';
import { useDebounce } from './useDebounce';

/**
 * Centralised complaint filter state.
 * Returns filter values, setters, and the constructed API query string.
 */
export const useComplaintFilters = () => {
  const [statusFilter, setStatusFilter] = useState('');
  const [overdueFilter, setOverdueFilter] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [urgencyFilter, setUrgencyFilter] = useState('');

  const debouncedSearch = useDebounce(searchTerm, 350);

  const buildQueryString = useCallback(() => {
    const params = new URLSearchParams();
    if (statusFilter)  params.set('status', statusFilter);
    if (overdueFilter) params.set('overdue', 'true');
    if (urgencyFilter) params.set('urgency', urgencyFilter);
    return params.toString();
  }, [statusFilter, overdueFilter, urgencyFilter]);

  /** Apply client-side search on a list of complaint objects */
  const applySearch = useCallback((complaints) => {
    if (!debouncedSearch) return complaints;
    const term = debouncedSearch.toLowerCase();
    return complaints.filter(c =>
      c.title?.toLowerCase().includes(term) ||
      String(c.id).includes(term) ||
      c.department?.name?.toLowerCase().includes(term) ||
      c.city?.toLowerCase().includes(term)
    );
  }, [debouncedSearch]);

  const resetFilters = useCallback(() => {
    setStatusFilter('');
    setOverdueFilter(false);
    setSearchTerm('');
    setUrgencyFilter('');
  }, []);

  const hasActiveFilters = !!(statusFilter || overdueFilter || urgencyFilter || debouncedSearch);

  return {
    statusFilter, setStatusFilter,
    overdueFilter, setOverdueFilter,
    searchTerm, setSearchTerm,
    urgencyFilter, setUrgencyFilter,
    debouncedSearch,
    buildQueryString,
    applySearch,
    resetFilters,
    hasActiveFilters,
  };
};

export default useComplaintFilters;
