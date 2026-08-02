import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LoadingSkeleton } from '../components/LoadingSkeleton';
import { FileText, ChevronRight, Calendar, Search, Filter } from 'lucide-react';
import './OfficerDashboard.css';

export const OfficerComplaints = () => {
  const { user, apiFetch } = useAuth();
  const navigate = useNavigate();

  const [complaints, setComplaints] = useState([]);
  const [loading, setLoading] = useState(true);

  // Filters
  const [statusFilter, setStatusFilter] = useState('');
  const [overdueFilter, setOverdueFilter] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  const loadComplaints = async () => {
    setLoading(true);
    try {
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
      console.error('Error loading officer complaints:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadComplaints();
  }, [statusFilter, overdueFilter]);

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
        <LoadingSkeleton type="table" />
      </div>
    );
  }

  return (
    <div className="officer-dashboard-container">
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

export default OfficerComplaints;
