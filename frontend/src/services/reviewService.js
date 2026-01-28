import api from './api';

export const reviewService = {
  async getFeedback(interactionId) {
    const response = await api.get(`/api/review/${interactionId}`);
    return response.data;
  },
  async submitFeedback(interactionId, payload) {
    const response = await api.post(`/api/review/${interactionId}`, payload);
    return response.data;
  },
};
