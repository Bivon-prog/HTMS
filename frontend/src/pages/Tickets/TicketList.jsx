import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Chip,
  Stack,
  Pagination,
  CircularProgress,
  Alert,
} from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';
import { useQuery } from 'react-query';
import { useNavigate } from 'react-router-dom';
import { Add, Search, FilterList } from '@mui/icons-material';
import toast from 'react-hot-toast';
import ticketService from '../../services/ticketService';

const TicketList = () => {
  const navigate = useNavigate();
  const [filters, setFilters] = useState({
    search: '',
    status: '',
    priority: '',
    category: '',
    page: 1,
  });

  const {
    data: ticketsData,
    isLoading,
    error,
    refetch,
  } = useQuery(
    ['tickets', filters],
    () => ticketService.getTickets(filters),
    {
      keepPreviousData: true,
    }
  );

  const columns = [
    {
      field: 'ticket_number',
      headerName: 'Ticket #',
      width: 140,
      renderCell: (params) => (
        <Button
          variant="text"
          color="primary"
          onClick={() => navigate(`/tickets/${params.row.id}`)}
        >
          {params.value}
        </Button>
      ),
    },
    {
      field: 'title',
      headerName: 'Title',
      width: 250,
      flex: 1,
    },
    {
      field: 'status',
      headerName: 'Status',
      width: 120,
      renderCell: (params) => (
        <Chip
          label={params.value}
          color={getStatusColor(params.value)}
          size="small"
        />
      ),
    },
    {
      field: 'priority',
      headerName: 'Priority',
      width: 100,
      renderCell: (params) => (
        <Chip
          label={params.value}
          color={getPriorityColor(params.value)}
          size="small"
        />
      ),
    },
    {
      field: 'category_name',
      headerName: 'Category',
      width: 120,
    },
    {
      field: 'requester_name',
      headerName: 'Requester',
      width: 150,
    },
    {
      field: 'agent_name',
      headerName: 'Assigned Agent',
      width: 150,
    },
    {
      field: 'created_at',
      headerName: 'Created',
      width: 120,
      renderCell: (params) => new Date(params.value).toLocaleDateString(),
    },
    {
      field: 'is_overdue',
      headerName: 'Overdue',
      width: 80,
      renderCell: (params) => (
        params.value && (
          <Chip label="Overdue" color="error" size="small" />
        )
      ),
    },
  ];

  const getStatusColor = (status) => {
    switch (status) {
      case 'Open': return 'default';
      case 'Assigned': return 'info';
      case 'In_Progress': return 'warning';
      case 'Resolved': return 'success';
      case 'Closed': return 'secondary';
      default: return 'default';
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'Low': return 'success';
      case 'Medium': return 'info';
      case 'High': return 'warning';
      case 'Critical': return 'error';
      default: return 'default';
    }
  };

  const handleFilterChange = (field, value) => {
    setFilters(prev => ({
      ...prev,
      [field]: value,
      page: 1, // Reset to first page when filters change
    }));
  };

  const handlePageChange = (newPage) => {
    setFilters(prev => ({
      ...prev,
      page: newPage,
    }));
  };

  if (error) {
    return (
      <Alert severity="error" sx={{ mt: 2 }}>
        Error loading tickets: {error.message}
      </Alert>
    );
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Tickets
        </Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => navigate('/tickets/create')}
        >
          Create Ticket
        </Button>
      </Box>

      {/* Filters */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Filters
          </Typography>
          <Stack direction="row" spacing={2} alignItems="center">
            <TextField
              placeholder="Search tickets..."
              value={filters.search}
              onChange={(e) => handleFilterChange('search', e.target.value)}
              InputProps={{
                startAdornment: <Search />,
              }}
              sx={{ minWidth: 250 }}
            />
            
            <FormControl sx={{ minWidth: 150 }}>
              <InputLabel>Status</InputLabel>
              <Select
                value={filters.status}
                label="Status"
                onChange={(e) => handleFilterChange('status', e.target.value)}
              >
                <MenuItem value="">All</MenuItem>
                <MenuItem value="Open">Open</MenuItem>
                <MenuItem value="Assigned">Assigned</MenuItem>
                <MenuItem value="In_Progress">In Progress</MenuItem>
                <MenuItem value="Resolved">Resolved</MenuItem>
                <MenuItem value="Closed">Closed</MenuItem>
              </Select>
            </FormControl>

            <FormControl sx={{ minWidth: 150 }}>
              <InputLabel>Priority</InputLabel>
              <Select
                value={filters.priority}
                label="Priority"
                onChange={(e) => handleFilterChange('priority', e.target.value)}
              >
                <MenuItem value="">All</MenuItem>
                <MenuItem value="Low">Low</MenuItem>
                <MenuItem value="Medium">Medium</MenuItem>
                <MenuItem value="High">High</MenuItem>
                <MenuItem value="Critical">Critical</MenuItem>
              </Select>
            </FormControl>

            <FormControl sx={{ minWidth: 150 }}>
              <InputLabel>Category</InputLabel>
              <Select
                value={filters.category}
                label="Category"
                onChange={(e) => handleFilterChange('category', e.target.value)}
              >
                <MenuItem value="">All</MenuItem>
                <MenuItem value="1">IT</MenuItem>
                <MenuItem value="2">HR</MenuItem>
                <MenuItem value="3">Facilities</MenuItem>
              </Select>
            </FormControl>

            <Button
              variant="outlined"
              startIcon={<FilterList />}
              onClick={() => refetch()}
            >
              Apply Filters
            </Button>
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
          ) : (
            <DataGrid
              rows={ticketsData?.results || []}
              columns={columns}
              pageSize={20}
              rowsPerPageOptions={[20]}
              disableSelectionOnClick
              autoHeight
              getRowId={(row) => row.id}
              sx={{ border: 'none' }}
            />
          )}
        </CardContent>
      </Card>

      {/* Pagination */}
      {ticketsData?.count > 0 && (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
          <Pagination
            count={Math.ceil(ticketsData.count / 20)}
            page={filters.page}
            onChange={(e, page) => handlePageChange(page)}
            color="primary"
          />
        </Box>
      )}
    </Box>
  );
};

export default TicketList;
