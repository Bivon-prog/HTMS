import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box, Card, CardContent, Typography, Button, TextField,
  Chip, CircularProgress, Alert, Stack, FormControl,
  InputLabel, Select, MenuItem,
} from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';
import { Add, Search, Warning } from '@mui/icons-material';
import { useQuery } from 'react-query';
import axios from 'axios';
import authService from '../../services/authService';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
const api = axios.create({ baseURL: API_BASE_URL });
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

const AssetList = () => {
  const navigate = useNavigate();
  const user = authService.getCurrentUser();
  const [filters, setFilters] = useState({ search: '', status: '' });

  const { data, isLoading, error } = useQuery(
    ['assets', filters],
    async () => {
      const res = await api.get('/assets/', { params: filters });
      return res.data;
    }
  );

  const canManageAssets = ['Mission_Admin', 'HQ_Super_Admin'].includes(user?.role);

  const columns = [
    {
      field: 'inventory_tag', headerName: 'Inventory Tag', width: 150,
      renderCell: (p) => (
        <Button variant="text" onClick={() => navigate(`/assets/${p.row.id}`)}>{p.value}</Button>
      ),
    },
    { field: 'device_type', headerName: 'Device Type', width: 130 },
    {
      field: 'make_model', headerName: 'Make / Model', width: 180,
      valueGetter: (p) => `${p.row.make || ''} ${p.row.model || ''}`.trim() || '—',
    },
    { field: 'operating_system', headerName: 'OS', width: 130 },
    { field: 'assigned_user_name', headerName: 'Assigned To', width: 150 },
    { field: 'mission_name', headerName: 'Mission', width: 150 },
    {
      field: 'status', headerName: 'Status', width: 110,
      renderCell: (p) => {
        const colors = { Active: 'success', Maintenance: 'warning', Retired: 'default', Lost: 'error' };
        return <Chip label={p.value} color={colors[p.value] || 'default'} size="small" />;
      },
    },
    {
      field: 'needs_replacement', headerName: 'Needs Replacement', width: 160,
      renderCell: (p) => p.value ? <Chip icon={<Warning />} label="Yes" color="error" size="small" /> : null,
    },
    {
      field: 'warranty_expiry_date', headerName: 'Warranty Expiry', width: 140,
      renderCell: (p) => p.value ? new Date(p.value).toLocaleDateString() : '—',
    },
  ];

  if (error) return <Alert severity="error">Error loading assets: {error.message}</Alert>;

  const rows = data?.results || data || [];

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">Assets</Typography>
        {canManageAssets && (
          <Button variant="contained" startIcon={<Add />} onClick={() => navigate('/assets/create')}>
            Add Asset
          </Button>
        )}
      </Box>

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Stack direction="row" spacing={2}>
            <TextField
              placeholder="Search by tag, type, make..."
              value={filters.search}
              onChange={(e) => setFilters(p => ({ ...p, search: e.target.value }))}
              InputProps={{ startAdornment: <Search sx={{ mr: 1, color: 'text.secondary' }} /> }}
              sx={{ minWidth: 280 }}
            />
            <FormControl sx={{ minWidth: 150 }}>
              <InputLabel>Status</InputLabel>
              <Select value={filters.status} label="Status" onChange={(e) => setFilters(p => ({ ...p, status: e.target.value }))}>
                <MenuItem value="">All</MenuItem>
                <MenuItem value="Active">Active</MenuItem>
                <MenuItem value="Maintenance">Maintenance</MenuItem>
                <MenuItem value="Retired">Retired</MenuItem>
                <MenuItem value="Lost">Lost</MenuItem>
              </Select>
            </FormControl>
          </Stack>
        </CardContent>
      </Card>

      <Card>
        <CardContent sx={{ p: 0 }}>
          {isLoading ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}><CircularProgress /></Box>
          ) : (
            <DataGrid
              rows={rows}
              columns={columns}
              pageSize={20}
              rowsPerPageOptions={[20]}
              disableSelectionOnClick
              autoHeight
              sx={{ border: 'none' }}
            />
          )}
        </CardContent>
      </Card>
    </Box>
  );
};

export default AssetList;
