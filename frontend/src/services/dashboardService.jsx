import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

const dashboardService = {
  getOverview: async () => {
    const response = await api.get('/dashboard/overview/');
    return response.data;
  },

  getTrends: async () => {
    const response = await api.get('/dashboard/trends/');
    return response.data;
  },

  getMissionStatistics: async () => {
    const response = await api.get('/dashboard/missions/');
    return response.data;
  },

  getAgentPerformance: async () => {
    const response = await api.get('/dashboard/agents/');
    return response.data;
  },
};

export default dashboardService;
