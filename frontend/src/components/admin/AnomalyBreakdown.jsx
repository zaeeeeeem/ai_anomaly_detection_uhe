import React from 'react';
import './AnomalyBreakdown.css';

export const AnomalyBreakdown = ({ data, loading }) => {
  if (loading) {
    return (
      <div className="anomaly-breakdown empty">
        <p>Loading...</p>
      </div>
    );
  }

  if (!data || !data.breakdown || data.breakdown.length === 0) {
    return (
      <div className="anomaly-breakdown empty">
        <p>No anomalies detected yet</p>
      </div>
    );
  }

  const breakdown = data.breakdown;
  const total = breakdown.reduce((sum, item) => sum + item.count, 0);

  const categoryConfig = {
    UNSAFE_ADVICE: { label: 'Unsafe Advice', color: '#dc2626' },
    HALLUCINATION: { label: 'Hallucination', color: '#ea580c' },
    CONTEXT_MISMATCH: { label: 'Context Mismatch', color: '#d97706' },
    POOR_QUALITY: { label: 'Poor Quality', color: '#ca8a04' },
    CONFIDENCE_ISSUE: { label: 'Confidence Issue', color: '#2563eb' },
    NONE: { label: 'Other', color: '#6b7280' }
  };

  return (
    <div className="anomaly-breakdown">
      <h3>Anomalies by Category</h3>
      <div className="breakdown-stats">
        <span className="total-count">{total}</span>
        <span className="total-label">Total Anomalies</span>
      </div>
      <div className="breakdown-list">
        {breakdown.map((item) => {
          const config = categoryConfig[item.category] || categoryConfig.NONE;
          const percentage = total > 0 ? ((item.count / total) * 100).toFixed(1) : 0;

          return (
            <div key={item.category} className="breakdown-item">
              <div className="item-header">
                <span className="item-label">
                  <span
                    className="color-dot"
                    style={{ backgroundColor: config.color }}
                  />
                  {config.label}
                </span>
                <span className="item-count">{item.count}</span>
              </div>
              <div className="item-bar">
                <div
                  className="item-fill"
                  style={{
                    width: `${percentage}%`,
                    backgroundColor: config.color
                  }}
                />
              </div>
              <div className="item-percentage">{percentage}%</div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
