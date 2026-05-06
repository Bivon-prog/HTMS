import React from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Paper,
  CircularProgress,
  Alert,
} from '@mui/material';
import { useQuery } from 'react-query';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
} from 'recharts';
import {
  SupportAgent as TicketIcon,
  CheckCircle as ResolvedIcon,
  Schedule as InProgressIcon,
  Warning as OverdueIcon,
} from '@mui/icons-material';
import dashboardService from '../../services/dashboardService';

const Dashboard = () => {
  const {
    data: overviewData,
    isLoading: overviewLoading,
    error: overviewError,
  } = useQuery('dashboard-overview', () => dashboardService.getOverview());

  const {
    data: trendsData,
    isLoading: trendsLoading,
  } = useQuery('dashboard-trends', () => dashboardService.getTrends());

  const COLORS = ['#1976d2', '#dc004e', '#ff9800', '#4caf50', '#9c27b0'];

  const StatCard = ({ title, value, icon: Icon, color }) => (
    <Card>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Box>
            <Typography color="textSecondary" gutterBottom variant="overline">
              {title}
            </Typography>
            <Typography variant="h4" component="div">
              {value}
            </Typography>
          </Box>
          <Box sx={{ color }}>
            <Icon sx={{ fontSize: 40 }} />
          </Box>
        </Box>
      </CardContent>
    </Card>
  );

  if (overviewError) {
    return (
      <Alert severity="error" sx={{ mt: 2 }}>
        Error loading dashboard data: {overviewError.message}
      </Alert>
    );
  }

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Dashboard
      </Typography>

      {/* Overview Statistics */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Tickets"
            value={overviewData?.overview?.total_tickets || 0}
            icon={TicketIcon}
            color="#1976d2"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Open Tickets"
            value={overviewData?.overview?.open_tickets || 0}
            icon={TicketIcon}
            color="#dc004e"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="In Progress"
            value={overviewData?.overview?.in_progress_tickets || 0}
            icon={InProgressIcon}
            color="#ff9800"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Resolved"
            value={overviewData?.overview?.resolved_tickets || 0}
            icon={ResolvedIcon}
            color="#4caf50"
          />
        </Grid>
      </Grid>

      {/* Charts */}
      <Grid container spacing={3}>
        {/* Priority Distribution */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Tickets by Priority
            </Typography>
            {overviewLoading ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
                <CircularProgress />
              </Box>
            ) : (
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={[
                      { name: 'Low', value: overviewData?.by_priority?.low || 0 },
                      { name: 'Medium', value: overviewData?.by_priority?.medium || 0 },
                      { name: 'High', value: overviewData?.by_priority?.high || 0 },
                      { name: 'Critical', value: overviewData?.by_priority?.critical || 0 },
                    ]}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, value }) => `${name}: ${value}`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {[
                      { name: 'Low', value: overviewData?.by_priority?.low || 0 },
                      { name: 'Medium', value: overviewData?.by_priority?.medium || 0 },
                      { name: 'High', value: overviewData?.by_priority?.high || 0 },
                      { name: 'Critical', value: overviewData?.by_priority?.critical || 0 },
                    ].map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            )}
          </Paper>
        </Grid>

        {/* Status Distribution */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Tickets by Status
            </Typography>
            {overviewLoading ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
                <CircularProgress />
              </Box>
            ) : (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart
                  data={[
                    { status: 'Open', count: overviewData?.by_status?.open || 0 },
                    { status: 'Assigned', count: overviewData?.by_status?.assigned || 0 },
                    { status: 'In Progress', count: overviewData?.by_status?.in_progress || 0 },
                    { status: 'Resolved', count: overviewData?.by_status?.resolved || 0 },
                    { status: 'Closed', count: overviewData?.by_status?.closed || 0 },
                  ]}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="status" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="count" fill="#1976d2" />
                </BarChart>
              </ResponsiveContainer>
            )}
          </Paper>
        </Grid>

        {/* Ticket Trends */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Ticket Creation Trends (Last 30 Days)
            </Typography>
            {trendsLoading ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
                <CircularProgress />
              </Box>
            ) : (
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={trendsData || []}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="count" stroke="#1976d2" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            )}
          </Paper>
        </Grid>

        {/* Performance Metrics */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Performance Metrics
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                <Typography variant="body1">Average Resolution Time</Typography>
                <Typography variant="body1" fontWeight="bold">
                  {overviewData?.performance?.average_resolution_hours || 'N/A'} hours
                </Typography>
              </Box>
              <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                <Typography variant="body1">SLA Compliance Rate</Typography>
                <Typography variant="body1" fontWeight="bold">
                  {overviewData?.performance?.sla_compliance_rate || 'N/A'}%
                </Typography>
              </Box>
              <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                <Typography variant="body1">Overdue Tickets</Typography>
                <Typography variant="body1" fontWeight="bold" color="error">
                  {overviewData?.overview?.overdue_tickets || 0}
                </Typography>
              </Box>
            </Box>
          </Paper>
        </Grid>

        {/* Recent Activity */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Recent Activity (Last 7 Days)
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                <Typography variant="body1">New Tickets</Typography>
                <Typography variant="body1" fontWeight="bold">
                  {overviewData?.recent_activity?.new_tickets || 0}
                </Typography>
              </Box>
              <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                <Typography variant="body1">Resolved Tickets</Typography>
                <Typography variant="body1" fontWeight="bold" color="success.main">
                  {overviewData?.recent_activity?.resolved_tickets || 0}
                </Typography>
              </Box>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
