import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { AdminLayout } from '../components/admin/AdminLayout';
import { AnomalyBreakdown } from '../components/admin/AnomalyBreakdown';
import { metricsService } from '../services/metricsService';
import './AdminHome.css';

export const AdminHome = () => {
  const [metrics, setMetrics] = useState(null);
  const [anomalyBreakdown, setAnomalyBreakdown] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadMetrics = async () => {
      setLoading(true);
      try {
        const [metricsData, breakdownData] = await Promise.all([
          metricsService.getMetrics(),
          metricsService.getAnomalyBreakdown('all')
        ]);
        setMetrics(metricsData);
        setAnomalyBreakdown(breakdownData);
      } catch (error) {
        console.error('Failed to load metrics:', error);
      } finally {
        setLoading(false);
      }
    };

    loadMetrics();
  }, []);

  const formatDuration = (seconds) => {
    if (!seconds) return '—';
    const mins = Math.round(seconds / 60);
    if (mins < 60) return `${mins} min`;
    const hours = Math.round(mins / 60);
    return `${hours} hr`;
  };

  const flaggedRate = metrics ? `${Math.round(metrics.flagged_rate * 100)}%` : '—';

  return (
    <AdminLayout
      title="Admin Home"
      subtitle="Monitor safety signals and review flagged interactions"
    >
      <div className="metrics-grid">
        <div className="metric-card">
          <span className="metric-label">Total interactions</span>
          <strong>{loading ? '...' : metrics?.total_interactions ?? 0}</strong>
        </div>
        <div className="metric-card">
          <span className="metric-label">Flag rate</span>
          <strong>{loading ? '...' : flaggedRate}</strong>
        </div>
        <div className="metric-card">
          <span className="metric-label">Reviewed items</span>
          <strong>{loading ? '...' : metrics?.reviewed_count ?? 0}</strong>
        </div>
        <div className="metric-card">
          <span className="metric-label">Avg review time</span>
          <strong>{loading ? '...' : formatDuration(metrics?.avg_review_time_seconds)}</strong>
        </div>
        <div className="metric-card">
          <span className="metric-label">Volume (24h)</span>
          <strong>{loading ? '...' : metrics?.volume?.last_24h ?? 0}</strong>
        </div>
        <div className="metric-card">
          <span className="metric-label">Volume (7d)</span>
          <strong>{loading ? '...' : metrics?.volume?.last_7d ?? 0}</strong>
        </div>
      </div>

      <AnomalyBreakdown data={anomalyBreakdown} loading={loading} />

      <div className="admin-home-grid">
        <div className="admin-home-card">
          <h3>Flagged for Review</h3>
          <p>See the highest risk conversations that need human review.</p>
          <Link className="admin-link" to="/admin/flagged-review">
            Open flagged queue
          </Link>
        </div>
        <div className="admin-home-card">
          <h3>All Interactions</h3>
          <p>Browse the full audit trail across all users.</p>
          <Link className="admin-link" to="/admin/all-interactions">
            View interactions
          </Link>
        </div>
        <div className="admin-home-card">
          <h3>Customer Lookup</h3>
          <p>Inspect interactions for a specific patient account.</p>
          <Link className="admin-link" to="/admin/customer-interactions">
            Find a customer
          </Link>
        </div>
      </div>
      <div className="admin-home-panel">
        <h4>Workflow Tips</h4>
        <ul>
          <li>Start with flagged items to reduce safety risk exposure.</li>
          <li>Use customer lookup for repeat high-risk behavior.</li>
          <li>Leave detailed reviewer comments to train improvements.</li>
        </ul>
      </div>
    </AdminLayout>
  );
};
