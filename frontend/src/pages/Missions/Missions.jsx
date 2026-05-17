import React, { useState } from 'react';
import {
  Box, Card, CardContent, Typography, Button, TextField,
  Chip, CircularProgress, Alert, Stack, FormControl,
  InputLabel, Select, MenuItem,
} from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';
import { Search } from '@mui/icons-material';
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

const Missions = () => {
  const user = authService.getCurrentUser();
  const [filters, setFilters] = useState({ search: '', region: '', status: '' });

  const { data, isLoading, error } = useQuery(
    ['missions', filters],
    async () => { const res = await api.get('/missions/', { params: filters }); return res.data; }
  );

  const columns = [
    { field: 'name', headerName: 'Mission Name', width: 220 },
    { field: 'city', headerName: 'City', width: 130 },
    { field: 'country', headerName: 'Country', width: 150 },
    { field: 'region', headerName: 'Region', width: 130 },
    { field: 'timezone', headerName: 'Timezone', width: 180 },
    {
      field: 'working_hours', headerName: 'Working Hours', width: 160,
      valueGetter: (p) => `${p.row.work_start_time || ''} – ${p.row.work_end_time || ''}`,
    },
    {
      field: 'mission_admin_id', headerName: 'Mission Admin', width: 210,
      renderCell: (p) => {
        const name = p.row.mission_admin_name;
        const id = p.row.mission_admin_id;
        if (!id) return <Typography variant="caption" color="text.disabled">— Unassigned</Typography>;
        return (
          <Box>
            <Typography variant="body2" sx={{ lineHeight: 1.2 }}>{name || 'Unknown'}</Typography>
            <Typography variant="caption" color="text.secondary" sx={{ fontFamily: 'monospace' }}>{id}</Typography>
          </Box>
        );
      },
    },
    {
      field: 'status', headerName: 'Status', width: 100,
      renderCell: (p) => <Chip label={p.value} color={p.value === 'Active' ? 'success' : 'default'} size="small" />,
    },
  ];

  if (error) return <Alert severity="error">Error loading missions</Alert>;

  const rows = data?.results || data || [];

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">Missions ({rows.length})</Typography>
      </Box>

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Stack direction="row" spacing={2}>
            <TextField
              placeholder="Search missions..."
              value={filters.search}
              onChange={(e) => setFilters(p => ({ ...p, search: e.target.value }))}
              InputProps={{ startAdornment: <Search sx={{ mr: 1, color: 'text.secondary' }} /> }}
              sx={{ minWidth: 280 }}
            />
            <FormControl sx={{ minWidth: 150 }}>
              <InputLabel>Region</InputLabel>
              <Select value={filters.region} label="Region" onChange={(e) => setFilters(p => ({ ...p, region: e.target.value }))}>
                <MenuItem value="">All</MenuItem>
                <MenuItem value="Africa">Africa</MenuItem>
                <MenuItem value="Europe">Europe</MenuItem>
                <MenuItem value="Americas">Americas</MenuItem>
                <MenuItem value="Asia">Asia</MenuItem>
                <MenuItem value="Middle_East">Middle East</MenuItem>
                <MenuItem value="Multilateral">Multilateral</MenuItem>
              </Select>
            </FormControl>
            <FormControl sx={{ minWidth: 130 }}>
              <InputLabel>Status</InputLabel>
              <Select value={filters.status} label="Status" onChange={(e) => setFilters(p => ({ ...p, status: e.target.value }))}>
                <MenuItem value="">All</MenuItem>
                <MenuItem value="Active">Active</MenuItem>
                <MenuItem value="Inactive">Inactive</MenuItem>
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
            <DataGrid rows={rows} columns={columns} pageSize={25} rowsPerPageOptions={[25, 50]}
              disableSelectionOnClick autoHeight sx={{ border: 'none' }} />
          )}
        </CardContent>
      </Card>
    </Box>
  );
};

export default Missions;
