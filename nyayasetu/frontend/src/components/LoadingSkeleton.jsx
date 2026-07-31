import React from 'react';
import './LoadingSkeleton.css';

export const LoadingSkeleton = ({ type = 'card', count = 1 }) => {
  const renderSkeleton = () => {
    switch (type) {
      case 'table':
        return (
          <div className="skeleton-table">
            <div className="skeleton-table-header shimmer"></div>
            {[...Array(5)].map((_, i) => (
              <div key={i} className="skeleton-table-row shimmer"></div>
            ))}
          </div>
        );
      case 'chart':
        return (
          <div className="skeleton-chart-container">
            <div className="skeleton-chart-title shimmer"></div>
            <div className="skeleton-chart-body shimmer"></div>
          </div>
        );
      case 'map':
        return <div className="skeleton-map shimmer"></div>;
      case 'detail':
        return (
          <div className="skeleton-detail">
            <div className="skeleton-title shimmer"></div>
            <div className="skeleton-meta shimmer"></div>
            <div className="skeleton-desc shimmer"></div>
            <div className="skeleton-box shimmer"></div>
          </div>
        );
      case 'card':
      default:
        return (
          <div className="skeleton-cards-grid">
            {[...Array(count)].map((_, i) => (
              <div key={i} className="skeleton-card">
                <div className="skeleton-card-img shimmer"></div>
                <div className="skeleton-card-title shimmer"></div>
                <div className="skeleton-card-text shimmer"></div>
                <div className="skeleton-card-text-short shimmer"></div>
              </div>
            ))}
          </div>
        );
    }
  };

  return <div className="skeleton-wrapper">{renderSkeleton()}</div>;
};
export default LoadingSkeleton;
