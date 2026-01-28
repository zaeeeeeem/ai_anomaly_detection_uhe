import api from './api';

export const chatService = {
  async sendMessage(conversationId, payload) {
    const response = await api.post(`/api/chat/${conversationId}/message`, payload);
    return response.data;
  },

  async getGeminiModels() {
    const response = await api.get('/api/chat/models/gemini');
    return response.data;
  },

  async getOllamaModels() {
    const response = await api.get('/api/chat/models/ollama');
    return response.data;
  },

  async getOllamaStatus() {
    const response = await api.get('/api/chat/ollama/status');
    return response.data;
  },
};
