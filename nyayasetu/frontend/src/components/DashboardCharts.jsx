import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { Doughnut, Bar } from 'react-chartjs-2';

// Register necessary ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

export const StatusDistributionChart = ({ stats }) => {
  // stats expected format: { resolved, pending, escalated, failures }
  const data = {
    labels: ['Resolved', 'Pending', 'Escalated', 'Admin Failure'],
    datasets: [
      {
        data: [
          stats.resolved || 0,
          stats.pending || 0,
          stats.escalated || 0,
          stats.failures || 0
        ],
        backgroundColor: ['#128807', '#ff9933', '#1e3a8a', '#dc2626'],
        borderColor: ['#ffffff', '#ffffff', '#ffffff', '#ffffff'],
        borderWidth: 2,
        hoverOffset: 8,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          usePointStyle: true,
          padding: 20,
          font: {
            family: "'Inter', sans-serif",
            size: 12,
            weight: '600'
          },
          color: '#1e293b'
        }
      },
      tooltip: {
        backgroundColor: '#ffffff',
        titleColor: '#0f172a',
        bodyColor: '#475569',
        borderColor: '#e2e8f0',
        borderWidth: 1,
        padding: 12,
        boxPadding: 6,
        usePointStyle: true,
        callbacks: {
          label: (context) => {
            const val = context.raw || 0;
            return ` ${context.label}: ${val} grievances`;
          }
        }
      }
    },
    cutout: '70%'
  };

  return (
    <div style={{ height: '300px', width: '100%', position: 'relative' }}>
      <Doughnut data={data} options={options} />
      <table className="sr-only">
        <caption>Grievance Status Distribution Data</caption>
        <thead>
          <tr>
            <th>Status</th>
            <th>Count</th>
          </tr>
        </thead>
        <tbody>
          <tr><td>Resolved</td><td>{stats.resolved || 0}</td></tr>
          <tr><td>Pending</td><td>{stats.pending || 0}</td></tr>
          <tr><td>Escalated</td><td>{stats.escalated || 0}</td></tr>
          <tr><td>Admin Failure</td><td>{stats.failures || 0}</td></tr>
        </tbody>
      </table>
    </div>
  );
};

export const DepartmentPerformanceChart = ({ departments = [] }) => {
  const data = {
    labels: departments.map(d => d.name),
    datasets: [
      {
        label: 'Transparency Score (%)',
        data: departments.map(d => d.transparencyScore),
        backgroundColor: 'rgba(18, 136, 7, 0.85)',
        hoverBackgroundColor: '#128807',
        borderRadius: 6,
        borderWidth: 0,
      },
      {
        label: 'Admin Failures',
        data: departments.map(d => d.failureCount),
        backgroundColor: 'rgba(220, 38, 38, 0.85)',
        hoverBackgroundColor: '#dc2626',
        borderRadius: 6,
        borderWidth: 0,
      }
    ]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          usePointStyle: true,
          padding: 20,
          font: {
            family: "'Inter', sans-serif",
            size: 12,
            weight: '600'
          },
          color: '#1e293b'
        }
      },
      tooltip: {
        backgroundColor: '#ffffff',
        titleColor: '#0f172a',
        bodyColor: '#475569',
        borderColor: '#e2e8f0',
        borderWidth: 1,
        padding: 12,
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        grid: {
          color: '#f1f5f9',
        },
        ticks: {
          font: { family: "'Inter', sans-serif" },
          color: '#64748b'
        }
      },
      x: {
        grid: {
          display: false
        },
        ticks: {
          font: { family: "'Inter', sans-serif", weight: '600' },
          color: '#1e293b'
        }
      }
    }
  };

  return (
    <div style={{ height: '300px', width: '100%', position: 'relative' }}>
      <Bar data={data} options={options} />
      <table className="sr-only">
        <caption>Department Performance Data</caption>
        <thead>
          <tr>
            <th>Department</th>
            <th>Transparency Score</th>
            <th>Admin Failures</th>
          </tr>
        </thead>
        <tbody>
          {departments.map((d, index) => (
            <tr key={index}>
              <td>{d.name}</td>
              <td>{d.transparencyScore}%</td>
              <td>{d.failureCount}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
