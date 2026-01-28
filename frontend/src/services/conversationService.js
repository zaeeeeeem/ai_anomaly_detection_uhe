import api from './api';

export const conversationService = {
  async createConversation(payload) {
    const response = await api.post('/api/conversations', payload);
    return response.data;
  },

  async getConversations() {
    const response = await api.get('/api/conversations');
    return response.data;
  },

  async getConversation(id) {
    const response = await api.get(`/api/conversations/${id}`);
    return response.data;
  },

  async updateConversation(id, payload) {
    const response = await api.put(`/api/conversations/${id}`, payload);
    return response.data;
  },

  async deleteConversation(id) {
    await api.delete(`/api/conversations/${id}`);
  },

  async getMessages(id) {
    const response = await api.get(`/api/conversations/${id}/messages`);
    return response.data;
  },
};
