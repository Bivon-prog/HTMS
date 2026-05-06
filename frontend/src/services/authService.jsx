import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Add response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/auth/refresh/`, {
            refresh: refreshToken,
          });

          const { access } = response.data.token;
          localStorage.setItem('access_token', access);

          // Retry the original request
          originalRequest.headers.Authorization = `Bearer ${access}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // Refresh failed, logout user
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

const authService = {
  login: async (email, password) => {
    const response = await api.post('/auth/login/', { email, password });
    const { token, user } = response.data;
    
    localStorage.setItem('access_token', token.access);
    localStorage.setItem('refresh_token', token.refresh);
    localStorage.setItem('user', JSON.stringify(user));
    
    return { token, user };
  },

  logout: async () => {
    try {
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        await api.post('/auth/logout/', { refresh: refreshToken });
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user');
    }
  },

  verifyToken: async () => {
    const response = await api.get('/auth/verify/');
    return response.data;
  },

  getCurrentUser: () => {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  },

  updateProfile: async (userData) => {
    const response = await api.patch('/auth/profile/', userData);
    const updatedUser = response.data.user;
    localStorage.setItem('user', JSON.stringify(updatedUser));
    return updatedUser;
  },

  passwordResetRequest: async (email) => {
    const response = await api.post('/auth/password-reset/', { email });
    return response.data;
  },

  passwordResetConfirm: async (token, password) => {
    const response = await api.post('/auth/password-reset-confirm/', { token, password });
    return response.data;
  },
};

export default authService;
