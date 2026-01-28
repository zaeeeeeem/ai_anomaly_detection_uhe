import api from './api';

export const metricsService = {
  async getMetrics() {
    const response = await api.get('/api/admin/metrics');
    return response.data;
  },

  async getEnhancedMetrics() {
    const response = await api.get('/api/admin/metrics/enhanced');
    return response.data;
  },

  async getAnomalyBreakdown(timePeriod = 'all') {
    const response = await api.get('/api/admin/analytics/anomaly-breakdown', {
      params: { time_period: timePeriod }
    });
    return response.data;
  },
};
