import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box, Card, CardContent, Typography, Button, Chip,
  Grid, Stack, CircularProgress, Alert, Divider,
} from '@mui/material';
import { ArrowBack, Warning } from '@mui/icons-material';
import { useQuery } from 'react-query';
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
const api = axios.create({ baseURL: API_BASE_URL });
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

const AssetDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const { data: asset, isLoading, error } = useQuery(
    ['asset', id],
    async () => { const res = await api.get(`/assets/${id}/`); return res.data; }
  );

  const { data: history = [] } = useQuery(
    ['asset-history', id],
    async () => { const res = await api.get(`/assets/${id}/history/`); return res.data.results || res.data; }
  );

  if (isLoading) return <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}><CircularProgress /></Box>;
  if (error) return <Alert severity="error">Error loading asset</Alert>;
  if (!asset) return <Alert severity="warning">Asset not found</Alert>;

  const statusColors = { Active: 'success', Maintenance: 'warning', Retired: 'default', Lost: 'error' };

  return (
    <Box>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 3, gap: 2 }}>
        <Button startIcon={<ArrowBack />} onClick={() => navigate('/assets')}>Back</Button>
        <Typography variant="h5">{asset.inventory_tag} — {asset.device_type}</Typography>
        {asset.needs_replacement && <Chip icon={<Warning />} label="Needs Replacement" color="error" />}
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>Asset Details</Typography>
              <Stack spacing={1.5}>
                {[
                  ['Inventory Tag', asset.inventory_tag],
                  ['Device Type', asset.device_type],
                  ['Make', asset.make || '—'],
                  ['Model', asset.model || '—'],
                  ['Operating System', asset.operating_system || '—'],
                  ['OS Version', asset.os_version || '—'],
                  ['Location', asset.location_within_mission || '—'],
                  ['Mission', asset.mission_name],
                  ['Assigned To', asset.assigned_user_name || 'Unassigned'],
                  ['Purchase Date', asset.purchase_date ? new Date(asset.purchase_date).toLocaleDateString() : '—'],
                  ['Warranty Expiry', asset.warranty_expiry_date ? new Date(asset.warranty_expiry_date).toLocaleDateString() : '—'],
                ].map(([label, value]) => (
                  <Box key={label} sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography variant="body2" color="text.secondary">{label}</Typography>
                    <Typography variant="body2">{value}</Typography>
                  </Box>
                ))}
                <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                  <Typography variant="body2" color="text.secondary">Status</Typography>
                  <Chip label={asset.status} color={statusColors[asset.status]} size="small" />
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                  <Typography variant="body2" color="text.secondary">Out of Warranty</Typography>
                  <Chip label={asset.is_out_of_warranty ? 'Yes' : 'No'} color={asset.is_out_of_warranty ? 'error' : 'success'} size="small" />
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                  <Typography variant="body2" color="text.secondary">Tickets (last 90 days)</Typography>
                  <Typography variant="body2" color={asset.ticket_count_90_days > 3 ? 'error' : 'inherit'}>
                    {asset.ticket_count_90_days}
                  </Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>Ticket History</Typography>
              <Divider sx={{ mb: 2 }} />
              {history.length === 0 ? (
                <Typography color="text.secondary">No tickets raised against this asset.</Typography>
              ) : (
                history.map((h) => (
                  <Box key={h.id} sx={{ mb: 1, p: 1.5, bgcolor: 'grey.50', borderRadius: 1 }}>
                    <Typography variant="body2" fontWeight="bold">{h.ticket_number}</Typography>
                    <Typography variant="body2" color="text.secondary">{h.ticket_title}</Typography>
                    <Typography variant="caption" color="text.secondary">
                      {new Date(h.created_at).toLocaleDateString()}
                    </Typography>
                  </Box>
                ))
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default AssetDetail;
