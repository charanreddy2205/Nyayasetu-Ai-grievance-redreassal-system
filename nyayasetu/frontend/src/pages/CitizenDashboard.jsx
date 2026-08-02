import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LoadingSkeleton } from '../components/LoadingSkeleton';
import { Badge, StatCard, EmptyState, SearchBar, Button } from '../components/ui';
import {
  PlusCircle, FileText, CheckCircle, Clock,
  AlertTriangle, ChevronRight, Calendar, Filter, RefreshCw
} from 'lucide-react';
import { useComplaintFilters } from '../hooks/useComplaintFilters';
import './CitizenDashboard.css';

export const CitizenDashboard = () => {
  const { user, apiFetch } = useAuth();
  const navigate = useNavigate();

  const [stats, setStats] = useState(null);
  const [complaints, setComplaints] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [fetchError, setFetchError] = useState('');

  const {
    statusFilter, setStatusFilter,
    overdueFilter, setOverdueFilter,
    searchTerm, setSearchTerm,
    buildQueryString,
    applySearch,
    resetFilters,
    hasActiveFilters,
  } = useComplaintFilters();

  const loadData = useCallback(async (silent = false) => {
    if (!silent) setLoading(true);
    else setRefreshing(true);
    setFetchError('');

    try {
      const qs = buildQueryString();
      const [statsRes, complaintsRes] = await Promise.all([
        apiFetch('/api/dashboard/stats/'),
        apiFetch(`/api/complaints/${qs ? '?' + qs : ''}`),
      ]);

      if (statsRes.ok) {
        const d = await statsRes.json();
        const normalizedStats = d?.user || d?.data?.user || d?.data || d || { total: 0, resolved: 0, pending: 0, escalated: 0, overdue: 0 };
        setStats(normalizedStats);
      }
      if (complaintsRes.ok) {
        const d = await complaintsRes.json();
        const complaintsPayload = d?.results || d?.complaints || d?.data?.complaints || d?.data || [];
        setComplaints(Array.isArray(complaintsPayload) ? complaintsPayload : []);
      } else {
        setFetchError('Failed to load grievances. Please try again.');
      }
    } catch {
      setFetchError('Network error. Please check your connection.');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, [apiFetch, buildQueryString]);

  useEffect(() => { loadData(); }, [loadData]);

  const filteredComplaints = applySearch(complaints);
  const s = stats || { total: 0, resolved: 0, pending: 0, escalated: 0, overdue: 0 };

  if (loading) {
    return (
      <div className="citizen-dashboard-container">
        <LoadingSkeleton type="card" count={4} />
        <div style={{ marginTop: '2rem' }}><LoadingSkeleton type="table" /></div>
      </div>
    );
  }

  return (
    <div className="citizen-dashboard-container">
      {/* Live region for screen readers */}
      <div role="status" aria-live="polite" className="sr-only">
        {refreshing ? 'Refreshing grievances…' : ''}
      </div>

      {/* Welcome banner */}
      <section className="welcome-banner" aria-label="Welcome section">
        <div className="welcome-info">
          <h1 style={{ margin: 0, fontSize: 'var(--font-size-2xl)', color: 'var(--text-dark)' }}>
            Welcome, {user?.firstName} {user?.lastName}
          </h1>
          <p className="welcome-sub">Grievance Desk &bull; Citizen Portal</p>
        </div>
        <div className="welcome-actions">
          <Button
            variant="secondary"
            size="sm"
            onClick={() => loadData(true)}
            disabled={refreshing}
            loading={refreshing}
            aria-label="Refresh grievances"
          >
            <RefreshCw size={15} aria-hidden="true" />
            {refreshing ? 'Refreshing…' : 'Refresh'}
          </Button>
          <Link to="/complaints/lodge" className="btn-lodge-g" aria-label="Lodge a new grievance">
            <PlusCircle size={17} aria-hidden="true" />
            Lodge New Grievance
          </Link>
        </div>
      </section>

      {/* Stats row */}
      <section aria-label="Grievance statistics" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 'var(--space-4)', marginBottom: 'var(--space-6)' }}>
        <StatCard icon={FileText}     label="Total Lodged"   value={s.total}                     accentColor="var(--primary-blue-light)" />
        <StatCard icon={Clock}        label="Active Cases"   value={s.pending + s.escalated}      accentColor="var(--saffron)" />
        <StatCard icon={CheckCircle}  label="Resolved"       value={s.resolved}                   accentColor="var(--green)" />
        <StatCard icon={AlertTriangle} label="Overdue Cases" value={s.overdue} warning accentColor="#ef4444" />
      </section>

      {/* Error state */}
      {fetchError && (
        <div role="alert" style={{
          padding: 'var(--space-4)', marginBottom: 'var(--space-4)',
          backgroundColor: 'var(--status-escalated-bg)', color: 'var(--status-escalated-text)',
          borderRadius: 'var(--radius-sm)', border: '1px solid var(--status-escalated-border)',
          fontSize: 'var(--font-size-sm)',
        }}>
          {fetchError}
        </div>
      )}


    </div>
  );
};

export default CitizenDashboard;
