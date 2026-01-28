import api from './api';

export const authService = {
  async signup(data) {
    const response = await api.post('/api/auth/signup', data);
    return response.data;
  },

  async login(data) {
    const response = await api.post('/api/auth/login', data);
    return response.data;
  },

  async getCurrentUser() {
    const response = await api.get('/api/auth/me');
    return response.data;
  },

  logout() {
    localStorage.removeItem('access_token');
  },
};
