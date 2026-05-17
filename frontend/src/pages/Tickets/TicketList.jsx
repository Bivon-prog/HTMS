import React, { useState, useEffect } from 'react';
import {
  Box, Card, CardContent, Typography, Button, TextField,
  Select, MenuItem, FormControl, InputLabel, Chip, Stack,
  CircularProgress, Alert, Tab, Tabs, Badge,
} from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';
import { useQuery } from 'react-query';
import { useNavigate, useLocation } from 'react-router-dom';
import { Add, Search, FilterList } from '@mui/icons-material';
import ticketService from '../../services/ticketService';
import authService from '../../services/authService';

const STATUS_COLORS = {
  Open: 'default', Assigned: 'info', In_Progress: 'warning',
  Resolved: 'success', Closed: 'secondary',
};
const PRIORITY_COLORS = {
  Low: 'success', Medium: 'info', High: 'warning', Critical: 'error',
};

const TicketList = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const user = authService.getCurrentUser();
  const isAgent = ['Agent', 'Mission_Admin', 'HQ_Super_Admin'].includes(user?.role);

  // Read queue param from URL (?queue=mine | ?queue=open)
  const queueParam = new URLSearchParams(location.search).get('queue') || 'all';
  const [activeTab, setActiveTab] = useState(queueParam);

  const [filters, setFilters] = useState({
    search: '', status: '', priority: '', page: 1,
  });

  // Sync tab when URL changes (sidebar clicks)
  useEffect(() => {
    setActiveTab(queueParam);
    setFilters(f => ({ ...f, page: 1 }));
  }, [queueParam]);

  const buildParams = () => {
    const p = { ...filters };
    if (activeTab === 'mine') p.assigned_agent = user?.id;
    if (activeTab === 'open') p.status = 'Open';
    return p;
  };

  const { data: ticketsData, isLoading, error, refetch } = useQuery(
    ['tickets', filters, activeTab],
    () => ticketService.getTickets(buildParams()),
    { keepPreviousData: true }
  );

  const handleTabChange = (_, val) => {
    setActiveTab(val);
    setFilters(f => ({ ...f, status: '', page: 1 }));
    // Update URL without full navigation
    const params = val === 'all' ? '' : `?queue=${val}`;
    navigate(`/tickets${params}`, { replace: true });
  };

  const handleFilterChange = (field, value) => {
    setFilters(prev => ({ ...prev, [field]: value, page: 1 }));
  };

  const columns = [
    {
      field: 'ticket_number', headerName: 'Ticket #', width: 140,
      renderCell: (p) => (
        <Button variant="text" color="primary" onClick={() => navigate(`/tickets/${p.row.id}`)}>
          {p.value}
        </Button>
      ),
    },
    { field: 'title', headerName: 'Title', width: 250, flex: 1 },
    {
      field: 'status', headerName: 'Status', width: 120,
      renderCell: (p) => (
        <Chip label={p.value?.replace('_', ' ')} color={STATUS_COLORS[p.value] || 'default'} size="small" />
      ),
    },
    {
      field: 'priority', headerName: 'Priority', width: 100,
      renderCell: (p) => (
        <Chip label={p.value} color={PRIORITY_COLORS[p.value] || 'default'} size="small" />
      ),
    },
    { field: 'category_name', headerName: 'Category', width: 120 },
    { field: 'mission_name', headerName: 'Mission', width: 150 },
    {
      field: 'submission_display', headerName: 'Submitted By', width: 180,
      renderCell: (p) => (
        <Typography variant="body2" noWrap title={p.value}>{p.value}</Typography>
      ),
    },
    {
      field: 'agent_name', headerName: 'Assigned Agent', width: 150,
      renderCell: (p) => p.value
        ? <Typography variant="body2">{p.value}</Typography>
        : <Typography variant="caption" color="text.disabled">Unassigned</Typography>,
    },
    {
      field: 'created_at', headerName: 'Created', width: 110,
      renderCell: (p) => new Date(p.value).toLocaleDateString(),
    },
    {
      field: 'is_overdue', headerName: 'SLA', width: 80,
      renderCell: (p) => p.value
        ? <Chip label="Overdue" color="error" size="small" />
        : null,
    },
  ];

  if (error) {
    return <Alert severity="error" sx={{ mt: 2 }}>Error loading tickets: {error.message}</Alert>;
  }

  const rows = ticketsData?.results || [];
  const totalCount = ticketsData?.count || 0;

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">Tickets</Typography>
        <Button variant="contained" startIcon={<Add />} onClick={() => navigate('/tickets/create')}>
          Create Ticket
        </Button>
      </Box>

      {/* Queue Tabs — only for agents & admins */}
      {isAgent && (
        <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
          <Tabs value={activeTab} onChange={handleTabChange}>
            <Tab label="All Tickets" value="all" />
            <Tab
              label={
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                  My Queue
                  {activeTab === 'mine' && rows.length > 0 && (
                    <Badge badgeContent={totalCount} color="primary" max={99} />
                  )}
                </Box>
              }
              value="mine"
            />
            <Tab label="Open Queue" value="open" />
          </Tabs>
        </Box>
      )}

      {/* Filters */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Stack direction="row" spacing={2} alignItems="center" flexWrap="wrap">
            <TextField
              placeholder="Search tickets..."
              value={filters.search}
              onChange={(e) => handleFilterChange('search', e.target.value)}
              InputProps={{ startAdornment: <Search sx={{ mr: 0.5, color: 'text.secondary' }} /> }}
              sx={{ minWidth: 240 }}
              size="small"
            />
            <FormControl sx={{ minWidth: 130 }} size="small">
              <InputLabel>Status</InputLabel>
              <Select value={filters.status} label="Status"
                onChange={(e) => handleFilterChange('status', e.target.value)}
                disabled={activeTab === 'open'}>
                <MenuItem value="">All</MenuItem>
                <MenuItem value="Open">Open</MenuItem>
                <MenuItem value="Assigned">Assigned</MenuItem>
                <MenuItem value="In_Progress">In Progress</MenuItem>
                <MenuItem value="Resolved">Resolved</MenuItem>
                <MenuItem value="Closed">Closed</MenuItem>
              </Select>
            </FormControl>
            <FormControl sx={{ minWidth: 120 }} size="small">
              <InputLabel>Priority</InputLabel>
              <Select value={filters.priority} label="Priority"
                onChange={(e) => handleFilterChange('priority', e.target.value)}>
                <MenuItem value="">All</MenuItem>
                <MenuItem value="Low">Low</MenuItem>
                <MenuItem value="Medium">Medium</MenuItem>
                <MenuItem value="High">High</MenuItem>
                <MenuItem value="Critical">Critical</MenuItem>
              </Select>
            </FormControl>
            <Button variant="outlined" startIcon={<FilterList />} onClick={() => refetch()} size="small">
              Refresh
            </Button>
            <Typography variant="caption" color="text.secondary" sx={{ ml: 'auto !important' }}>
              {totalCount} ticket{totalCount !== 1 ? 's' : ''}
            </Typography>
          </Stack>
        </CardContent>
      </Card>

      {/* Tickets Table */}
      <Card>
        <CardContent sx={{ p: 0 }}>
          {isLoading ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
              <CircularProgress />
            </Box>
          ) : rows.length === 0 ? (
            <Box sx={{ p: 4, textAlign: 'center' }}>
              <Typography color="text.secondary">
                {activeTab === 'mine'
                  ? 'No tickets assigned to you.'
                  : activeTab === 'open'
                  ? 'No open tickets in your queue.'
                  : 'No tickets found.'}
              </Typography>
            </Box>
          ) : (
            <DataGrid
              rows={rows}
              columns={columns}
              pageSize={20}
              rowsPerPageOptions={[20]}
              disableSelectionOnClick
              autoHeight
              getRowId={(row) => row.id}
              sx={{ border: 'none' }}
              onPageChange={(page) => handleFilterChange('page', page + 1)}
            />
          )}
        </CardContent>
      </Card>
    </Box>
  );
};

export default TicketList;
