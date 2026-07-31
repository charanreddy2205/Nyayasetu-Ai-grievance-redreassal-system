import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { DashboardMap } from '../components/DashboardMap';
import { StatusDistributionChart, DepartmentPerformanceChart } from '../components/DashboardCharts';
import { LoadingSkeleton } from '../components/LoadingSkeleton';
import { FileText, CheckCircle, Clock, AlertTriangle, Shield, MapPin, BarChart3, Award } from 'lucide-react';
import './PublicDashboard.css';

export const PublicDashboard = () => {
  const { apiFetch } = useAuth();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchStats = async () => {
    try {
      const response = await apiFetch('/api/dashboard/stats/');
      if (response.ok) {
        const data = await response.json();
        setStats(data?.data || data);
      }
    } catch (error) {
      console.error('Error fetching stats:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  if (loading) {
    return (
      <div className="dashboard-page-container">
        <div className="skeleton-dashboard-grid">
          <LoadingSkeleton type="card" count={4} />
          <div style={{ marginTop: '2rem' }}><LoadingSkeleton type="map" /></div>
          <div className="skeleton-two-col" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', marginTop: '2rem' }}>
            <LoadingSkeleton type="chart" />
            <LoadingSkeleton type="chart" />
          </div>
        </div>
      </div>
    );
  }

  const global = stats || { total: 0, resolved: 0, pending: 0, escalated: 0, failures: 0 };
  const departments = stats?.departments || [];
  const states = stats?.states || [];
  const cities = stats?.cities || [];
  const mapPins = stats?.mapPins || [];

  return (
    <div className="dashboard-page-container">
      {/* Hero Welcome banner */}
      <section className="hero-banner">
        <div className="hero-content">
          <span className="gov-tag">Grievance Redressal Project Prototype</span>
          <h1 className="hero-title">Transparency Dashboard Project</h1>
          <p className="hero-subtitle">
            Demonstration of real-time public tracking of grievances, department accountability, and SLA resolutions.
          </p>
        </div>
        <div className="hero-accent-strip"></div>
      </section>

      {/* Numerical Counter Cards */}
      <div className="stats-counters-grid">
        <div className="counter-card total">
          <div className="counter-icon-wrap">
            <FileText size={24} />
          </div>
          <div className="counter-details">
            <h3 className="counter-value">{global.total}</h3>
            <span className="counter-label">Grievances Lodged</span>
          </div>
        </div>

        <div className="counter-card resolved">
          <div className="counter-icon-wrap">
            <CheckCircle size={24} />
          </div>
          <div className="counter-details">
            <h3 className="counter-value">{global.resolved}</h3>
            <span className="counter-label">Resolved Cases</span>
          </div>
        </div>

        <div className="counter-card pending">
          <div className="counter-icon-wrap">
            <Clock size={24} />
          </div>
          <div className="counter-details">
            <h3 className="counter-value">{global.pending + global.escalated}</h3>
            <span className="counter-label">Active / Pending</span>
          </div>
        </div>

        <div className="counter-card failure">
          <div className="counter-icon-wrap">
            <AlertTriangle size={24} />
          </div>
          <div className="counter-details">
            <h3 className="counter-value">{global.failures}</h3>
            <span className="counter-label">Admin Failures</span>
          </div>
        </div>
      </div>

      {/* Geospatial Map Row */}
      <section className="dashboard-section card-box">
        <div className="section-header">
          <div className="section-title-wrap">
            <MapPin className="section-icon text-blue" size={22} />
            <h2 className="section-title">Geospatial Grievance Map</h2>
          </div>
          <span className="section-badge">Interactive Grievance Clusters</span>
        </div>
        <div className="map-view-wrapper">
          <DashboardMap complaints={mapPins} />
        </div>
      </section>

      {/* Analytical Charts Row */}
      <div className="dashboard-row-two-col">
        <section className="dashboard-section card-box">
          <div className="section-header">
            <div className="section-title-wrap">
              <BarChart3 className="section-icon text-saffron" size={22} />
              <h2 className="section-title">Status Distribution</h2>
            </div>
          </div>
          <div className="chart-wrapper">
            <StatusDistributionChart stats={global} />
          </div>
        </section>

        <section className="dashboard-section card-box">
          <div className="section-header">
            <div className="section-title-wrap">
              <BarChart3 className="section-icon text-green" size={22} />
              <h2 className="section-title">Department Performance</h2>
            </div>
          </div>
          <div className="chart-wrapper">
            <DepartmentPerformanceChart departments={departments} />
          </div>
        </section>
      </div>

      {/* Regional Distributions */}
      <div className="dashboard-row-two-col">
        <section className="dashboard-section card-box">
          <div className="section-header">
            <div className="section-title-wrap">
              <Shield className="section-icon" size={22} />
              <h2 className="section-title">State-wise Distribution</h2>
            </div>
          </div>
          <div className="state-distribution-list">
            {states.length > 0 ? (
              states.map((s, idx) => {
                const maxVal = Math.max(...states.map(x => x.total));
                const pct = maxVal > 0 ? (s.total / maxVal) * 100 : 0;
                return (
                  <div key={idx} className="state-bar-row">
                    <span className="state-name">{s.state}</span>
                    <div className="state-bar-track">
                      <div 
                        className="state-bar-fill" 
                        style={{ width: `${pct}%` }}
                      ></div>
                    </div>
                    <span className="state-count-tag">{s.total}</span>
                  </div>
                );
              })
            ) : (
              <p className="no-data-text">No state-wise statistics available.</p>
            )}
          </div>
        </section>

        <section className="dashboard-section card-box">
          <div className="section-header">
            <div className="section-title-wrap">
              <Shield className="section-icon" size={22} />
              <h2 className="section-title">Top 10 Cities</h2>
            </div>
          </div>
          <div className="city-stats-table-wrapper">
            <table className="dashboard-mini-table">
              <thead>
                <tr>
                  <th>City</th>
                  <th className="text-center">Total Complaints</th>
                </tr>
              </thead>
              <tbody>
                {cities.length > 0 ? (
                  cities.map((c, idx) => (
                    <tr key={idx}>
                      <td className="font-bold">{c.city}</td>
                      <td className="text-center">
                        <span className="city-count-badge">{c.total}</span>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="2" className="text-center text-muted">No city statistics available.</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </section>
      </div>

      {/* Leaderboard Department Rankings */}
      <section className="dashboard-section card-box">
        <div className="section-header">
          <div className="section-title-wrap">
            <Award className="section-icon text-gold" size={22} />
            <h2 className="section-title">Department Rankings & Transparency</h2>
          </div>
          <span className="section-badge">Ordered by Transparency Score</span>
        </div>
        <div className="leaderboard-table-wrapper">
          <table className="dashboard-main-table">
            <thead>
              <tr>
                <th>Rank</th>
                <th>Department</th>
                <th className="text-center">Total Cases</th>
                <th className="text-center">Resolved Cases</th>
                <th className="text-center">Admin Failures</th>
                <th>Transparency Index</th>
              </tr>
            </thead>
            <tbody>
              {departments.length > 0 ? (
                departments.map((dept, idx) => {
                  const score = dept.transparencyScore;
                  let progressBarColor = 'green';
                  if (score < 50) progressBarColor = 'red';
                  else if (score < 80) progressBarColor = 'saffron';

                  return (
                    <tr key={dept.id}>
                      <td>
                        <span className="rank-badge">{idx + 1}</span>
                      </td>
                      <td>
                        <div className="dept-name-cell">{dept.name}</div>
                        <div className="dept-desc-cell">{dept.description}</div>
                      </td>
                      <td className="text-center font-semibold">{dept.totalComplaints}</td>
                      <td className="text-center">
                        <span className="status-badge success-light">{dept.resolvedCount}</span>
                      </td>
                      <td className="text-center">
                        <span className="status-badge danger-light">{dept.failureCount}</span>
                      </td>
                      <td>
                        <div className="transparency-progress-wrapper">
                          <div className="progress-bar-container">
                            <div 
                              className={`progress-bar-fill ${progressBarColor}`}
                              style={{ width: `${score}%` }}
                            ></div>
                          </div>
                          <span className={`score-label ${progressBarColor}-text`}>
                            {score.toFixed(1)}%
                          </span>
                        </div>
                      </td>
                    </tr>
                  );
                })
              ) : (
                <tr>
                  <td colSpan="6" className="text-center text-muted">No department statistics available.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
};

export default PublicDashboard;
