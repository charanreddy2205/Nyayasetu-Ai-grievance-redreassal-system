import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LoadingSkeleton } from '../components/LoadingSkeleton';
import { DashboardMap } from '../components/DashboardMap';
import { 
  FileText, CheckCircle, Clock, AlertTriangle, 
  ChevronRight, Calendar, Search, Filter, RefreshCw, MapPin
} from 'lucide-react';
import './OfficerDashboard.css';

export const OfficerDashboard = () => {
  const { user, apiFetch } = useAuth();
  const navigate = useNavigate();

  const [stats, setStats] = useState(null);
  const [complaints, setComplaints] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  // Filters
  const [statusFilter, setStatusFilter] = useState('');
  const [overdueFilter, setOverdueFilter] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  const loadOfficerData = async (isSilent = false) => {
    if (!isSilent) setLoading(true);
    else setRefreshing(true);

    try {
      // 1. Fetch Stats
      const statsRes = await apiFetch('/api/dashboard/stats/');
      if (statsRes.ok) {
        const statsData = await statsRes.json();
        const normalizedStats = statsData?.user || statsData?.data?.user || statsData?.data || statsData || { assigned: 0, overdue: 0, escalated: 0, resolved: 0, departmentName: '', departmentMapPins: [] };
        setStats(normalizedStats);
      }

      // 2. Fetch Complaints
      let url = '/api/complaints/';
      const params = [];
      if (statusFilter) params.push(`status=${statusFilter}`);
      if (overdueFilter) params.push('overdue=true');
      if (params.length > 0) {
        url += `?${params.join('&')}`;
      }

      const complaintsRes = await apiFetch(url);
      if (complaintsRes.ok) {
        const complaintsData = await complaintsRes.json();
        const complaintsPayload = complaintsData?.results || complaintsData?.complaints || complaintsData?.data?.complaints || complaintsData?.data || [];
        setComplaints(Array.isArray(complaintsPayload) ? complaintsPayload : []);
      }
    } catch (err) {
      console.error('Error loading officer dashboard data:', err);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    loadOfficerData();
  }, [statusFilter, overdueFilter]);

  const handleRefresh = () => {
    loadOfficerData(true);
  };

  const filteredComplaints = complaints.filter(c => 
    c.title.toLowerCase().includes(searchTerm.toLowerCase()) || 
    c.id.toString().includes(searchTerm) ||
    (c.address && c.address.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  const getStatusClass = (status) => {
    switch (status) {
      case 'resolved': return 'badge-resolved';
      case 'in_progress': return 'badge-progress';
      case 'pending': return 'badge-pending';
      case 'escalated': return 'badge-escalated';
      case 'administrative_failure': return 'badge-failure';
      default: return '';
    }
  };

  const getUrgencyClass = (urgency) => {
    switch (urgency) {
      case 'critical': return 'urgency-critical';
      case 'high': return 'urgency-high';
      case 'medium': return 'urgency-medium';
      case 'low': return 'urgency-low';
      default: return '';
    }
  };

  if (loading) {
    return (
      <div className="officer-dashboard-container">
        <LoadingSkeleton type="card" count={4} />
        <div style={{ marginTop: '2rem' }}><LoadingSkeleton type="map" /></div>
        <div style={{ marginTop: '2rem' }}><LoadingSkeleton type="table" /></div>
      </div>
    );
  }

  const officerStats = stats || { assigned: 0, overdue: 0, escalated: 0, resolved: 0, departmentName: '', departmentMapPins: [] };

  return (
    <div className="officer-dashboard-container">
      {/* Welcome Banner */}
      <section className="welcome-banner-officer">
        <div className="welcome-info">
          <h2>Welcome, Officer {user?.firstName} {user?.lastName}</h2>
          <p className="welcome-sub">
            Assigned App: <strong>{officerStats.departmentName || 'General'}</strong> redresses desk
          </p>
        </div>
        <div className="welcome-actions">
          <button onClick={handleRefresh} className="btn-refresh" disabled={refreshing}>
            <RefreshCw size={16} className={refreshing ? 'spin-icon' : ''} />
            {refreshing ? 'Refreshing...' : 'Refresh Queue'}
          </button>
        </div>
      </section>

      {/* Stats Counter Row */}
      <div className="officer-stats-row">
        <div className="o-stat-card">
          <div className="o-stat-icon blue-bg">
            <FileText size={20} />
          </div>
          <div className="o-stat-info">
            <h4>{officerStats.assigned}</h4>
            <span>Assigned Cases</span>
          </div>
        </div>

        <div className="o-stat-card">
          <div className="o-stat-icon orange-bg">
            <Clock size={20} />
          </div>
          <div className="o-stat-info">
            <h4>{officerStats.assigned - officerStats.resolved - officerStats.overdue}</h4>
            <span>Active Cases</span>
          </div>
        </div>

        <div className="o-stat-card">
          <div className="o-stat-icon green-bg">
            <CheckCircle size={20} />
          </div>
          <div className="o-stat-info">
            <h4>{officerStats.resolved}</h4>
            <span>Resolved Cases</span>
          </div>
        </div>

        <div className="o-stat-card warning-border">
          <div className="o-stat-icon red-bg">
            <AlertTriangle size={20} />
          </div>
          <div className="o-stat-info">
            <h4 className="red-text">{officerStats.overdue}</h4>
            <span className="red-text">SLA Breaches</span>
          </div>
        </div>
      </div>

      {/* Department Complaint Pins Map */}
      {officerStats.departmentMapPins && officerStats.departmentMapPins.length > 0 && (
        <section className="dashboard-section card-box">
          <div className="section-header">
            <div className="section-title-wrap">
              <MapPin className="section-icon text-blue" size={22} />
              <h2 className="section-title">Department Geospatial Queue</h2>
            </div>
            <span className="section-badge">{officerStats.departmentName} Department Boundaries</span>
          </div>
          <div className="map-view-wrapper" style={{ height: '350px' }}>
            <DashboardMap complaints={officerStats.departmentMapPins} />
          </div>
        </section>
      )}

      {/* Queue List Table */}
      <section className="complaints-list-section card-box">
        <div className="section-header-flex">
          <h3 className="section-title-c">Grievance Backlog &amp; Queue</h3>
          
          <div className="filter-controls-wrap">
            {/* Search Input */}
            <div className="search-bar-wrap">
              <Search className="search-icon-inside" size={16} />
              <input 
                type="text" 
                placeholder="Search by ID, title or address..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="search-input-field"
              />
            </div>

            {/* Status Filter */}
            <div className="filter-select-wrap">
              <Filter className="filter-icon-inside" size={16} />
              <select 
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="filter-select-field"
              >
                <option value="">All Statuses</option>
                <option value="pending">Pending</option>
                <option value="in_progress">In Progress</option>
                <option value="resolved">Resolved</option>
                <option value="escalated">Escalated</option>
                <option value="administrative_failure">Admin Failure</option>
              </select>
            </div>

            {/* Overdue Checkbox */}
            <label className="overdue-toggle-label">
              <input 
                type="checkbox"
                checked={overdueFilter}
                onChange={(e) => setOverdueFilter(e.target.checked)}
                className="overdue-checkbox"
              />
              <span>SLA Breached Only</span>
            </label>
          </div>
        </div>

        <div className="complaints-table-wrapper">
          {filteredComplaints.length > 0 ? (
            <table className="citizen-complaints-table">
              <thead>
                <tr>
                  <th>Grievance ID</th>
                  <th>Title &amp; Date</th>
                  <th>Location</th>
                  <th>Urgency</th>
                  <th>Deadline (SLA)</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredComplaints.map(complaint => (
                  <tr key={complaint.id} className="complaint-row-hover" onClick={() => navigate(`/complaints/${complaint.id}`)}>
                    <td className="bold-id">#{complaint.id}</td>
                    <td>
                      <div className="complaint-title-cell">{complaint.title}</div>
                      <div className="complaint-date-cell">
                        <Calendar size={12} />
                        <span>Lodged on {new Date(complaint.createdAt).toLocaleDateString()}</span>
                      </div>
                    </td>
                    <td>
                      <span className="location-cell" title={complaint.address}>
                        {complaint.city || 'Unknown'}, {complaint.state || ''}
                      </span>
                    </td>
                    <td>
                      <span className={`urgency-badge ${getUrgencyClass(complaint.urgencyLevel)}`}>
                        {complaint.urgencyLevel}
                      </span>
                      {complaint.sentimentScore != null && (
                        <div style={{ fontSize: '11px', marginTop: '4px', color: '#666', fontWeight: 500 }}>
                          Sentiment: {complaint.sentimentScore > 0 ? '+' : ''}{complaint.sentimentScore.toFixed(2)}
                        </div>
                      )}
                    </td>
                    <td>
                      {complaint.status === 'resolved' ? (
                        <span className="text-muted small">Resolved</span>
                      ) : complaint.isOverdue ? (
                        <span className="deadline-tag overdue font-bold">Overdue</span>
                      ) : complaint.slaDeadline ? (
                        <span className="deadline-tag small">
                          {new Date(complaint.slaDeadline).toLocaleDateString()} ({complaint.escalationLevel > 0 ? `Lvl ${complaint.escalationLevel}` : 'Normal'})
                        </span>
                      ) : (
                        <span className="text-muted small">No SLA</span>
                      )}
                    </td>
                    <td>
                      <span className={`status-pill ${getStatusClass(complaint.status)}`}>
                        {complaint.status ? complaint.status.replace(/_/g, ' ') : 'Pending'}
                      </span>
                    </td>
                    <td>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '4px', alignItems: 'center' }}>
                        <button className="btn-table-action" onClick={(e) => {
                          e.stopPropagation();
                          navigate(`/complaints/${complaint.id}`);
                        }}>
                          Review
                          <ChevronRight size={14} />
                        </button>
                        {(!complaint.assignedTo || complaint.assignedTo.username !== user?.username) && (
                          <span style={{ fontSize: '10px', color: '#888', fontWeight: '500', background: '#f5f5f5', padding: '2px 6px', borderRadius: '4px' }}>
                            Read Only
                          </span>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div className="no-complaints-fallback">
              <FileText size={48} className="fallback-icon" />
              <h4>Queue is Empty</h4>
              <p>Great job! There are no grievances matching the current filters.</p>
              {(statusFilter || overdueFilter || searchTerm) && (
                <button onClick={() => { setStatusFilter(''); setOverdueFilter(false); setSearchTerm(''); }} className="btn-clear-filters">
                  Clear Filters
                </button>
              )}
            </div>
          )}
        </div>
      </section>
    </div>
  );
};

export default OfficerDashboard;
