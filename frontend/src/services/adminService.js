import api from './api';

export const adminService = {
  async getUsers() {
    const response = await api.get('/api/admin/users');
    return response.data;
  },
  async getAllInteractions({ limit = 100, offset = 0 } = {}) {
    const response = await api.get('/api/admin/interactions', {
      params: { limit, offset },
    });
    return response.data;
  },
  async getFlaggedInteractions({ limit = 100, offset = 0 } = {}) {
    const response = await api.get('/api/admin/interactions/flagged', {
      params: { limit, offset },
    });
    return response.data;
  },
  async getUserInteractions(userId, { limit = 100, offset = 0 } = {}) {
    const response = await api.get(`/api/admin/interactions/user/${userId}`, {
      params: { limit, offset },
    });
    return response.data;
  },
  async getInteractionDetail(interactionId) {
    const response = await api.get(`/api/interactions/${interactionId}`);
    return response.data;
  },
  async getDetailedAnalysis(interactionId) {
    const response = await api.get(`/api/admin/interactions/${interactionId}/detailed`);
    return response.data;
  },
  async getAllAnomalies({ minScore = null, limit = 100 } = {}) {
    const params = { limit };
    if (minScore !== null) {
      params.min_score = minScore;
    }
    const response = await api.get('/api/admin/interactions/anomalies/all', { params });
    return response.data;
  },
  async getAnomaliesByCategory(category, { limit = 100 } = {}) {
    const response = await api.get('/api/admin/interactions/anomalies/by-category', {
      params: { category, limit }
    });
    return response.data;
  },
};
