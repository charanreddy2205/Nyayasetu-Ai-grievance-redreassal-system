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

      {/* Complaints list */}
      <section className="complaints-list-section card-box" aria-label="Grievance list">
        <div className="section-header-flex">
          <h2 className="section-title-c" style={{ margin: 0 }}>Track Your Grievances</h2>

          <div className="filter-controls-wrap">
            <SearchBar
              value={searchTerm}
              onChange={setSearchTerm}
              placeholder="Search by title, ID or department…"
              label="Search grievances"
              style={{ minWidth: 220 }}
            />

            <div className="filter-select-wrap">
              <Filter className="filter-icon-inside" size={15} aria-hidden="true" />
              <select
                value={statusFilter}
                onChange={e => setStatusFilter(e.target.value)}
                className="filter-select-field"
                aria-label="Filter by status"
              >
                <option value="">All Statuses</option>
                <option value="pending">Pending</option>
                <option value="in_progress">In Progress</option>
                <option value="resolved">Resolved</option>
                <option value="escalated">Escalated</option>
                <option value="administrative_failure">Admin Failure</option>
              </select>
            </div>

            <label className="overdue-toggle-label">
              <input
                type="checkbox"
                checked={overdueFilter}
                onChange={e => setOverdueFilter(e.target.checked)}
                className="overdue-checkbox"
                aria-label="Show only overdue SLA cases"
              />
              <span>Breached SLA Only</span>
            </label>
          </div>
        </div>

        <div className="complaints-table-wrapper">
          {filteredComplaints.length > 0 ? (
            <table
              className="citizen-complaints-table"
              aria-label="Your submitted grievances"
              aria-rowcount={filteredComplaints.length}
            >
              <caption className="sr-only">
                List of {filteredComplaints.length} grievances
              </caption>
              <thead>
                <tr>
                  <th scope="col">ID</th>
                  <th scope="col">Grievance Details</th>
                  <th scope="col">Department</th>
                  <th scope="col">Urgency</th>
                  <th scope="col">SLA Deadline</th>
                  <th scope="col">Status</th>
                  <th scope="col"><span className="sr-only">Actions</span></th>
                </tr>
              </thead>
              <tbody>
                {filteredComplaints.map(complaint => (
                  <tr
                    key={complaint.id}
                    className="complaint-row-hover"
                    onClick={() => navigate(`/complaints/${complaint.id}`)}
                    style={{ cursor: 'pointer' }}
                    tabIndex={0}
                    onKeyDown={e => e.key === 'Enter' && navigate(`/complaints/${complaint.id}`)}
                    aria-label={`Grievance ${complaint.id}: ${complaint.title}`}
                  >
                    <td className="bold-id">#{complaint.id}</td>
                    <td>
                      <div className="complaint-title-cell">{complaint.title}</div>
                      <div className="complaint-date-cell">
                        <Calendar size={12} aria-hidden="true" />
                        <span>Lodged {new Date(complaint.createdAt).toLocaleDateString()}</span>
                      </div>
                    </td>
                    <td>
                      <span className="dept-tag">
                        {complaint.department?.name || 'Processing…'}
                      </span>
                    </td>
                    <td>
                      <Badge variant="urgency" value={complaint.urgency} />
                    </td>
                    <td>
                      {complaint.status === 'resolved' ? (
                        <span className="text-muted small">Resolved</span>
                      ) : complaint.isOverdue ? (
                        <span className="deadline-tag overdue font-bold" aria-label="SLA Breached">Breached</span>
                      ) : complaint.slaDeadline ? (
                        <span className="deadline-tag small">{new Date(complaint.slaDeadline).toLocaleDateString()}</span>
                      ) : (
                        <span className="text-muted small">No SLA</span>
                      )}
                    </td>
                    <td>
                      <Badge variant="status" value={complaint.status} />
                    </td>
                    <td>
                      <button
                        className="btn-table-action"
                        onClick={e => { e.stopPropagation(); navigate(`/complaints/${complaint.id}`); }}
                        aria-label={`View details for grievance ${complaint.id}`}
                      >
                        View <ChevronRight size={13} aria-hidden="true" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <EmptyState
              icon={FileText}
              title={hasActiveFilters ? 'No Matching Grievances' : 'No Grievances Found'}
              description={
                hasActiveFilters
                  ? 'Try adjusting your filters to find what you\'re looking for.'
                  : 'You haven\'t submitted any grievances yet.'
              }
              actionLabel={hasActiveFilters ? 'Clear Filters' : 'Lodge Your First Grievance'}
              onAction={hasActiveFilters ? resetFilters : () => navigate('/complaints/lodge')}
            />
          )}
        </div>
      </section>
    </div>
  );
};

export default CitizenDashboard;
