import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LoadingSkeleton } from '../components/LoadingSkeleton';
import {
  ArrowLeft, Calendar, User, Shield, CheckCircle,
  Clock, AlertTriangle, AlertCircle, Sparkles, MessageSquare, Send, Image,
  X, CheckSquare, RefreshCw
} from 'lucide-react';
import './ComplaintDetail.css';

export const ComplaintDetail = () => {
  const { id } = useParams();
  const { user, apiFetch } = useAuth();

  const [complaint, setComplaint] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submittingComment, setSubmittingComment] = useState(false);
  const [updatingStatus, setUpdatingStatus] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Comment Form State
  const [commentText, setCommentText] = useState('');
  const [commentImage, setCommentImage] = useState(null);
  const [commentImagePreview, setCommentImagePreview] = useState(null);

  const fetchComplaintDetails = async () => {
    try {
      const response = await apiFetch(`/api/complaints/${id}/`);
      if (response.ok) {
        const data = await response.json();
        setComplaint(data?.data || data);
      } else {
        setError('You do not have permission to view this complaint, or it does not exist.');
      }
    } catch (err) {
      console.error(err);
      setError('Network error fetching grievance details.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchComplaintDetails();
  }, [id]);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setCommentImage(file);
      setCommentImagePreview(URL.createObjectURL(file));
    }
  };

  const handleRemoveImage = () => {
    setCommentImage(null);
    setCommentImagePreview(null);
  };

  const handleCommentSubmit = async (e) => {
    e.preventDefault();
    if (!commentText.trim()) return;

    setSubmittingComment(true);
    setError('');

    const formData = new FormData();
    formData.append('comment_text', commentText);
    if (commentImage) {
      formData.append('image', commentImage);
    }

    try {
      const response = await apiFetch(`/api/complaints/${id}/comments/`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          // Append comment to list locally
          setComplaint(prev => ({
            ...prev,
            comments: [...prev.comments, data.comment]
          }));
          setCommentText('');
          handleRemoveImage();
        } else {
          setError(data.error || 'Failed to submit comment.');
        }
      }
    } catch (err) {
      console.error(err);
      setError('Failed to post comment.');
    } finally {
      setSubmittingComment(false);
    }
  };

  const handleStatusUpdate = async (newStatus) => {
    setUpdatingStatus(true);
    setError('');
    setSuccess('');

    try {
      const response = await apiFetch(`/api/complaints/${id}/status/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ status: newStatus }),
      });

      const data = await response.json();
      if (response.ok && data.success) {
        setSuccess(`Complaint status updated to '${newStatus.replace('_', ' ')}' successfully!`);
        // Refresh details
        await fetchComplaintDetails();
      } else {
        setError(data.error || 'Failed to update status.');
      }
    } catch (err) {
      console.error(err);
      setError('Failed to update status.');
    } finally {
      setUpdatingStatus(false);
    }
  };

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
      <div className="complaint-detail-container">
        <LoadingSkeleton type="detail" />
      </div>
    );
  }

  if (error && !complaint) {
    return (
      <div className="complaint-detail-container text-center">
        <div className="alert-badge error" style={{ display: 'inline-flex', marginTop: '4rem' }}>
          <AlertCircle size={20} />
          <span>{error}</span>
        </div>
        <div style={{ marginTop: '2rem' }}>
          <Link to="/dashboard" className="btn-lodge-g">Return to Dashboard</Link>
        </div>
      </div>
    );
  }

  const isAssignedOfficer = complaint && user && complaint.assignedTo && complaint.assignedTo.username === user.username;

  return (
    <div className="complaint-detail-container">
      {/* Back button */}
      <div className="back-link-wrap">
        <Link to="/dashboard" className="btn-back">
          <ArrowLeft size={16} />
          Back to Dashboard
        </Link>
      </div>

      {/* Notifications */}
      {error && (
        <div className="alert-badge error">
          <AlertCircle size={20} />
          <span>{error}</span>
        </div>
      )}
      {success && (
        <div className="alert-badge success">
          <CheckCircle size={20} />
          <span>{success}</span>
        </div>
      )}

      {/* Layout Grid */}
      <div className="detail-layout-grid">
        
        {/* Left Column: Complaint Details & Timeline */}
        <div className="detail-left-column">
          
          {/* Main Info Card */}
          <section className="detail-card card-box">
            <div className="detail-card-header">
              <span className="complaint-id-badge">Grievance #{complaint.id}</span>
              <span className={`status-pill ${getStatusClass(complaint.status)}`}>
                {complaint.statusDisplay}
              </span>
            </div>

            <h1 className="complaint-title-h1">{complaint.title}</h1>
            
            <div className="complaint-meta-grid">
              <div className="meta-item">
                <Calendar size={16} />
                <span>Lodged: {new Date(complaint.createdAt).toLocaleString()}</span>
              </div>
              <div className="meta-item">
                <Shield size={16} />
                <span>Dept: {complaint.department?.name}</span>
              </div>
              <div className="meta-item">
                <User size={16} />
                <span>Assigned: {complaint.assignedTo ? `${complaint.assignedTo.username} (${complaint.assignedTo.role})` : 'Processing...'}</span>
              </div>
            </div>

            {/* AI Summary Banner */}
            {complaint.summary && (
              <div className="ai-summary-banner">
                <div className="ai-banner-heading">
                  <Sparkles size={16} className="spark-text" />
                  <span>AI Generated Executive Summary</span>
                </div>
                <p className="ai-summary-content">{complaint.summary}</p>
              </div>
            )}

            <div className="complaint-description-content">
              <h3 className="sub-section-title">Grievance Explanation</h3>
              <p className="description-text">{complaint.description}</p>
            </div>

            {/* Image Attachments */}
            {complaint.imageUrl && (
              <div className="complaint-image-attachment">
                <h3 className="sub-section-title">Lodged Image Attachment</h3>
                <div className="attachment-preview">
                  <img src={complaint.imageUrl} alt="Lodged complaint site photo" className="complaint-attached-image" />
                </div>
              </div>
            )}
          </section>

          {/* Timeline and History Logs */}
          <section className="detail-card card-box">
            <h3 className="sub-section-title">Timeline & Escalation History</h3>
            <div className="timeline-stepper">
              
              {/* Stepped Timeline: Node 1 (Lodge) */}
              <div className="timeline-step">
                <div className="timeline-node active">
                  <CheckCircle size={14} />
                </div>
                <div className="timeline-info">
                  <h4 className="timeline-step-title">Grievance Lodged</h4>
                  <p className="timeline-step-desc">Grievance registered in portal by citizen.</p>
                  <span className="timeline-step-date">{new Date(complaint.createdAt).toLocaleString()}</span>
                </div>
              </div>

              {/* Node 2 (Assign) */}
              {complaint.assignedTo && (
                <div className="timeline-step">
                  <div className="timeline-node active">
                    <User size={14} />
                  </div>
                  <div className="timeline-info">
                    <h4 className="timeline-step-title">Assigned to Officer</h4>
                    <p className="timeline-step-desc">Auto-assigned to officer <strong>{complaint.assignedTo.username}</strong> ({complaint.assignedTo.role}) in {complaint.department?.name}.</p>
                  </div>
                </div>
              )}

              {/* Escalation Log Nodes */}
              {complaint.logs && complaint.logs.map(log => (
                <div key={log.id} className="timeline-step">
                  <div className="timeline-node warning">
                    <AlertTriangle size={14} />
                  </div>
                  <div className="timeline-info">
                    <h4 className="timeline-step-title text-warning">SLA Breached - Escalated</h4>
                    <p className="timeline-step-desc">{log.reason}</p>
                    <span className="timeline-step-date">{new Date(log.escalatedAt).toLocaleString()}</span>
                  </div>
                </div>
              ))}

              {/* Status resolved/admin failures */}
              {complaint.status === 'resolved' && (
                <div className="timeline-step">
                  <div className="timeline-node success">
                    <CheckCircle size={14} />
                  </div>
                  <div className="timeline-info">
                    <h4 className="timeline-step-title text-green">Grievance Resolved</h4>
                    <p className="timeline-step-desc">Case marked as resolved. Redress completed.</p>
                    {complaint.resolvedAt && (
                      <span className="timeline-step-date">{new Date(complaint.resolvedAt).toLocaleString()}</span>
                    )}
                  </div>
                </div>
              )}

              {complaint.status === 'administrative_failure' && (
                <div className="timeline-step">
                  <div className="timeline-node failure">
                    <AlertTriangle size={14} />
                  </div>
                  <div className="timeline-info">
                    <h4 className="timeline-step-title text-red">Administrative Failure</h4>
                    <p className="timeline-step-desc">SLA escalation levels exhausted. Transparency score deducted.</p>
                  </div>
                </div>
              )}
            </div>
          </section>
        </div>

        {/* Right Column: Metadata, SLA Breaches, Action Bar, and Comments */}
        <div className="detail-right-column">
          
          {/* Metadata Card */}
          <div className="detail-card card-box bg-navy-card">
            <h3 className="sub-section-title text-white">Redressal SLA Status</h3>
            <div className="sla-card-content">
              <div className="sla-metric">
                <span className="sla-label">Urgency Level:</span>
                <span className={`urgency-badge ${getUrgencyClass(complaint.urgencyLevel)}`}>
                  {complaint.urgencyLevel}
                </span>
              </div>
              
              {complaint.sentimentScore != null && (
                <div className="sla-metric">
                  <span className="sla-label">Sentiment Score:</span>
                  <span className="sla-val-text">
                    {complaint.sentimentScore > 0 ? '+' : ''}{complaint.sentimentScore.toFixed(2)}
                  </span>
                </div>
              )}
              
              <div className="sla-metric">
                <span className="sla-label">SLA Deadline:</span>
                <span className="sla-val-text">
                  {complaint.slaDeadline ? new Date(complaint.slaDeadline).toLocaleDateString() : 'N/A'}
                </span>
              </div>

              {complaint.status !== 'resolved' && complaint.status !== 'administrative_failure' && (
                <div className="sla-alert-banner">
                  {complaint.isOverdue ? (
                    <div className="sla-status-tag danger">
                      <AlertTriangle size={16} />
                      <span>SLA breached! Case escalated.</span>
                    </div>
                  ) : (
                    <div className="sla-status-tag success">
                      <Clock size={16} />
                      <span>Active. Resolving within SLA window.</span>
                    </div>
                  )}
                </div>
              )}

              <div className="location-info-small">
                <h4 className="loc-title text-white">Location Details</h4>
                <p className="text-white-50">{complaint.address}</p>
                <div className="loc-meta text-white-50">
                  <span><strong>City:</strong> {complaint.city}</span>
                  <span><strong>Pincode:</strong> {complaint.pincode}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Officer Quick Actions Panel */}
          {isAssignedOfficer && (complaint.status === 'pending' || complaint.status === 'in_progress') && (
            <div className="detail-card card-box border-blue-panel">
              <h3 className="sub-section-title">Officer Actions</h3>
              <p className="desc-small">Update the current status of this grievance. Ensure you attach site verification photo updates in comments below.</p>
              
              <div className="action-buttons-flex">
                {complaint.status === 'pending' && (
                  <button 
                    onClick={() => handleStatusUpdate('in_progress')}
                    className="btn-action-status in-progress"
                    disabled={updatingStatus}
                  >
                    <RefreshCw size={16} className={updatingStatus ? 'spin-icon' : ''} />
                    Mark In Progress
                  </button>
                )}
                
                <button 
                  onClick={() => handleStatusUpdate('resolved')}
                  className="btn-action-status resolved"
                  disabled={updatingStatus}
                >
                  <CheckSquare size={16} />
                  Mark Resolved
                </button>
              </div>
            </div>
          )}

          {/* Communications & Comment Feed */}
          <div className="detail-card card-box">
            <h3 className="sub-section-title flex-align-icon">
              <MessageSquare size={18} className="text-blue" />
              Communication History ({complaint.comments ? complaint.comments.length : 0})
            </h3>
            
            <div className="comments-chat-feed">
              {complaint.comments && complaint.comments.length > 0 ? (
                complaint.comments.map(c => {
                  const isAuthorSelf = user && c.author === user.username;
                  return (
                    <div 
                      key={c.id} 
                      className={`chat-bubble-wrap ${isAuthorSelf ? 'self' : 'other'}`}
                    >
                      <div className="chat-bubble-meta">
                        <span className="author-name">{c.author}</span>
                        <span className="author-role-badge">{c.authorRole}</span>
                      </div>
                      <div className="chat-bubble-body">
                        <p>{c.commentText}</p>
                        {c.imageUrl && (
                          <div className="chat-comment-image-wrapper">
                            <a href={c.imageUrl} target="_blank" rel="noopener noreferrer">
                              <img src={c.imageUrl} alt="Comment attachment" className="chat-comment-img" />
                            </a>
                          </div>
                        )}
                      </div>
                      <span className="chat-bubble-time">
                        {new Date(c.createdAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </span>
                    </div>
                  );
                })
              ) : (
                <p className="no-comments-text text-muted">No messages or updates logged yet.</p>
              )}
            </div>

            {/* Write comment Form */}
            <form onSubmit={handleCommentSubmit} className="comment-input-form">
              <div className="comment-textarea-wrap">
                <textarea
                  rows={2}
                  placeholder="Post an update, response or upload photo verification..."
                  value={commentText}
                  onChange={(e) => setCommentText(e.target.value)}
                  disabled={submittingComment}
                  className="comment-textarea-field"
                />
              </div>

              {/* Image attachment preview */}
              {commentImagePreview && (
                <div className="comment-img-attachment-preview">
                  <img src={commentImagePreview} alt="Comment upload preview" />
                  <button type="button" onClick={handleRemoveImage} className="btn-close-attachment">
                    <X size={12} />
                  </button>
                </div>
              )}

              <div className="comment-actions-row">
                <div className="attachment-triggers">
                  <input
                    type="file"
                    id="comment-attachment"
                    accept="image/*"
                    onChange={handleFileChange}
                    className="hidden-file-input"
                    disabled={submittingComment}
                  />
                  <label htmlFor="comment-attachment" className="btn-attach-image" title="Attach Site Visit Photo">
                    <Image size={18} />
                    <span>Attach Photo</span>
                  </label>
                </div>

                <button 
                  type="submit" 
                  className="btn-send-comment"
                  disabled={submittingComment || !commentText.trim()}
                >
                  <Send size={14} />
                  {submittingComment ? 'Sending...' : 'Send'}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ComplaintDetail;
