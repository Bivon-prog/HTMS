import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Create axios instance with auth
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

const ticketService = {
  // Get tickets with filtering
  getTickets: async (params = {}) => {
    const response = await api.get('/tickets/', { params });
    return response.data;
  },

  // Get single ticket
  getTicket: async (id) => {
    const response = await api.get(`/tickets/${id}/`);
    return response.data;
  },

  // Create new ticket
  createTicket: async (ticketData) => {
    const response = await api.post('/tickets/', ticketData);
    return response.data;
  },

  // Update ticket status
  updateTicketStatus: async (id, status, comment = '') => {
    const response = await api.patch(`/tickets/${id}/status/`, { status, comment });
    return response.data;
  },

  // Assign ticket to agent
  assignTicket: async (id, agentId) => {
    const response = await api.patch(`/tickets/${id}/assign/`, { assigned_agent: agentId });
    return response.data;
  },

  // Escalate ticket to HQ
  escalateTicket: async (id, reason) => {
    const response = await api.post(`/tickets/${id}/escalate/`, { reason });
    return response.data;
  },

  // Get ticket comments
  getTicketComments: async (ticketId) => {
    const response = await api.get(`/tickets/${ticketId}/comments/`);
    return response.data;
  },

  // Add comment to ticket
  addTicketComment: async (ticketId, content, isInternal = false) => {
    const response = await api.post(`/tickets/${ticketId}/comments/`, {
      content,
      is_internal: isInternal,
    });
    return response.data;
  },

  // Get ticket attachments
  getTicketAttachments: async (ticketId) => {
    const response = await api.get(`/tickets/${ticketId}/attachments/`);
    return response.data;
  },

  // Upload attachment
  uploadAttachment: async (ticketId, file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post(`/tickets/${ticketId}/attachments/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Get ticket statistics
  getTicketStatistics: async () => {
    const response = await api.get('/tickets/statistics/');
    return response.data;
  },

  // Get audit log
  getAuditLog: async (ticketId) => {
    const url = ticketId ? `/tickets/${ticketId}/audit/` : '/tickets/audit/';
    const response = await api.get(url);
    return response.data;
  },
};

export default ticketService;
