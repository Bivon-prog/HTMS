import React, { useState } from 'react';
import {
  Box, Card, CardContent, Typography, Button, TextField,
  Chip, CircularProgress, Alert, Stack, FormControl,
  InputLabel, Select, MenuItem, Dialog, DialogTitle,
  DialogContent, DialogActions, Grid,
} from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';
import { Add, Search } from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { useForm, Controller } from 'react-hook-form';
import toast from 'react-hot-toast';
import axios from 'axios';
import authService from '../../services/authService';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
const api = axios.create({ baseURL: API_BASE_URL });
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

const ROLE_COLORS = {
  Requester: 'default', Agent: 'info',
  Mission_Admin: 'warning', HQ_Super_Admin: 'error',
};

const Users = () => {
  const queryClient = useQueryClient();
  const currentUser = authService.getCurrentUser();
  const [filters, setFilters] = useState({ search: '', role: '' });
  const [createDialog, setCreateDialog] = useState(false);

  const { data, isLoading, error } = useQuery(
    ['users', filters],
    async () => { const res = await api.get('/auth/', { params: filters }); return res.data; }
  );

  const { data: missions = [] } = useQuery('missions', async () => {
    const res = await api.get('/missions/');
    return res.data.results || res.data;
  });

  const { register, handleSubmit, control, reset, formState: { errors } } = useForm();

  const createMutation = useMutation(
    (data) => api.post('/auth/', data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('users');
        setCreateDialog(false);
        reset();
        toast.success('User created successfully');
      },
      onError: (err) => {
        const msg = Object.values(err.response?.data || {}).flat().join(', ') || 'Failed to create user';
        toast.error(msg);
      },
    }
  );

  const columns = [
    { field: 'full_name', headerName: 'Name', width: 200 },
    { field: 'email', headerName: 'Email', width: 220 },
    {
      field: 'role', headerName: 'Role', width: 150,
      renderCell: (p) => <Chip label={p.value?.replace('_', ' ')} color={ROLE_COLORS[p.value] || 'default'} size="small" />,
    },
    { field: 'department', headerName: 'Department', width: 120 },
    { field: 'mission_name', headerName: 'Mission', width: 180 },
    {
      field: 'is_active', headerName: 'Active', width: 90,
      renderCell: (p) => <Chip label={p.value ? 'Active' : 'Inactive'} color={p.value ? 'success' : 'default'} size="small" />,
    },
    {
      field: 'date_joined', headerName: 'Joined', width: 120,
      renderCell: (p) => new Date(p.value).toLocaleDateString(),
    },
  ];

  if (error) return <Alert severity="error">Error loading users</Alert>;

  const rows = data?.results || data || [];

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">Users</Typography>
        <Button variant="contained" startIcon={<Add />} onClick={() => setCreateDialog(true)}>
          Add User
        </Button>
      </Box>

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Stack direction="row" spacing={2}>
            <TextField
              placeholder="Search by name or email..."
              value={filters.search}
              onChange={(e) => setFilters(p => ({ ...p, search: e.target.value }))}
              InputProps={{ startAdornment: <Search sx={{ mr: 1, color: 'text.secondary' }} /> }}
              sx={{ minWidth: 280 }}
            />
            <FormControl sx={{ minWidth: 150 }}>
              <InputLabel>Role</InputLabel>
              <Select value={filters.role} label="Role" onChange={(e) => setFilters(p => ({ ...p, role: e.target.value }))}>
                <MenuItem value="">All</MenuItem>
                <MenuItem value="Requester">Requester</MenuItem>
                <MenuItem value="Agent">Agent</MenuItem>
                <MenuItem value="Mission_Admin">Mission Admin</MenuItem>
                <MenuItem value="HQ_Super_Admin">HQ Super Admin</MenuItem>
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
            <DataGrid rows={rows} columns={columns} pageSize={20} rowsPerPageOptions={[20]}
              disableSelectionOnClick autoHeight sx={{ border: 'none' }} />
          )}
        </CardContent>
      </Card>

      {/* Create User Dialog */}
      <Dialog open={createDialog} onClose={() => setCreateDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Create New User</DialogTitle>
        <form onSubmit={handleSubmit((d) => createMutation.mutate(d))}>
          <DialogContent>
            <Grid container spacing={2} sx={{ mt: 0 }}>
              <Grid item xs={6}>
                <TextField {...register('first_name', { required: 'Required' })} fullWidth label="First Name"
                  error={!!errors.first_name} helperText={errors.first_name?.message} />
              </Grid>
              <Grid item xs={6}>
                <TextField {...register('last_name', { required: 'Required' })} fullWidth label="Last Name"
                  error={!!errors.last_name} helperText={errors.last_name?.message} />
              </Grid>
              <Grid item xs={12}>
                <TextField {...register('email', { required: 'Required' })} fullWidth label="Email" type="email"
                  error={!!errors.email} helperText={errors.email?.message} />
              </Grid>
              <Grid item xs={12}>
                <TextField {...register('password', { required: 'Required', minLength: { value: 8, message: 'Min 8 chars' } })}
                  fullWidth label="Password" type="password" error={!!errors.password} helperText={errors.password?.message} />
              </Grid>
              <Grid item xs={12}>
                <TextField {...register('password_confirm', { required: 'Required' })}
                  fullWidth label="Confirm Password" type="password" />
              </Grid>
              <Grid item xs={6}>
                <FormControl fullWidth>
                  <InputLabel>Role</InputLabel>
                  <Controller name="role" control={control} defaultValue="Requester"
                    render={({ field }) => (
                      <Select {...field} label="Role">
                        <MenuItem value="Requester">Requester</MenuItem>
                        <MenuItem value="Agent">Agent</MenuItem>
                        <MenuItem value="Mission_Admin">Mission Admin</MenuItem>
                        {currentUser?.role === 'HQ_Super_Admin' && <MenuItem value="HQ_Super_Admin">HQ Super Admin</MenuItem>}
                      </Select>
                    )} />
                </FormControl>
              </Grid>
              <Grid item xs={6}>
                <FormControl fullWidth>
                  <InputLabel>Department</InputLabel>
                  <Controller name="department" control={control} defaultValue=""
                    render={({ field }) => (
                      <Select {...field} label="Department">
                        <MenuItem value="">None</MenuItem>
                        <MenuItem value="IT">IT</MenuItem>
                        <MenuItem value="HR">HR</MenuItem>
                        <MenuItem value="Facilities">Facilities</MenuItem>
                        <MenuItem value="Finance">Finance</MenuItem>
                        <MenuItem value="Admin">Admin</MenuItem>
                      </Select>
                    )} />
                </FormControl>
              </Grid>
              {currentUser?.role === 'HQ_Super_Admin' && (
                <Grid item xs={12}>
                  <FormControl fullWidth>
                    <InputLabel>Mission</InputLabel>
                    <Controller name="mission" control={control} defaultValue=""
                      render={({ field }) => (
                        <Select {...field} label="Mission">
                          <MenuItem value="">None (HQ)</MenuItem>
                          {missions.map((m) => (
                            <MenuItem key={m.id} value={m.id}>{m.name} — {m.city}, {m.country}</MenuItem>
                          ))}
                        </Select>
                      )} />
                  </FormControl>
                </Grid>
              )}
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => { setCreateDialog(false); reset(); }}>Cancel</Button>
            <Button type="submit" variant="contained" disabled={createMutation.isLoading}>Create</Button>
          </DialogActions>
        </form>
      </Dialog>
    </Box>
  );
};

export default Users;
