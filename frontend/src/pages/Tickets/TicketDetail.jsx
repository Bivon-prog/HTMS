import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box, Card, CardContent, Typography, Chip, Button, TextField,
  Divider, CircularProgress, Alert, Grid, Stack, Avatar,
  FormControlLabel, Switch, Dialog, DialogTitle, DialogContent,
  DialogActions, MenuItem, Select, FormControl, InputLabel,
} from '@mui/material';
import {
  ArrowBack, Send, AttachFile, Escalator, AssignmentInd, PersonAdd,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import toast from 'react-hot-toast';
import ticketService from '../../services/ticketService';
import authService from '../../services/authService';
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
const api = axios.create({ baseURL: API_BASE_URL });
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

const STATUS_COLORS = {
  Open: 'default', Assigned: 'info', In_Progress: 'warning',
  Resolved: 'success', Closed: 'secondary',
};
const PRIORITY_COLORS = {
  Low: 'success', Medium: 'info', High: 'warning', Critical: 'error',
};

const TicketDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const user = authService.getCurrentUser();

  const [comment, setComment] = useState('');
  const [isInternal, setIsInternal] = useState(false);
  const [statusDialog, setStatusDialog] = useState(false);
  const [newStatus, setNewStatus] = useState('');
  const [newStatusComment, setNewStatusComment] = useState('');
  const [escalateDialog, setEscalateDialog] = useState(false);
  const [escalateReason, setEscalateReason] = useState('');
  const [assignDialog, setAssignDialog] = useState(false);
  const [selectedAgent, setSelectedAgent] = useState('');

  const { data: ticket, isLoading, error } = useQuery(
    ['ticket', id],
    () => ticketService.getTicket(id)
  );

  // Load agents for the assignment picker (Mission Admin + HQ)
  const isAdmin = ['Mission_Admin', 'HQ_Super_Admin'].includes(user?.role);
  const { data: agentsList = [] } = useQuery(
    ['agents', ticket?.mission],
    async () => {
      const res = await api.get('/auth/', { params: { role: 'Agent' } });
      const all = res.data.results || res.data;
      // Also include Mission_Admin & HQ_Super_Admin who can resolve tickets
      const res2 = await api.get('/auth/', { params: { role: 'Mission_Admin' } });
      const admins = res2.data.results || res2.data;
      return [...all, ...admins];
    },
    { enabled: isAdmin && !!ticket }
  );

  const addCommentMutation = useMutation(
    ({ content, isInternal }) => ticketService.addTicketComment(id, content, isInternal),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['ticket', id]);
        setComment('');
        toast.success('Comment added');
      },
      onError: () => toast.error('Failed to add comment'),
    }
  );

  const updateStatusMutation = useMutation(
    ({ status, comment }) => ticketService.updateTicketStatus(id, status, comment),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['ticket', id]);
        setStatusDialog(false);
        toast.success('Status updated');
      },
      onError: () => toast.error('Failed to update status'),
    }
  );

  const escalateMutation = useMutation(
    (reason) => ticketService.escalateTicket(id, reason),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['ticket', id]);
        setEscalateDialog(false);
        setEscalateReason('');
        toast.success('Ticket escalated to HQ');
      },
      onError: () => toast.error('Failed to escalate ticket'),
    }
  );

  const assignToMeMutation = useMutation(
    () => ticketService.assignTicket(id, user?.id),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['ticket', id]);
        toast.success('Ticket assigned to you');
      },
      onError: () => toast.error('Failed to assign ticket'),
    }
  );

  const assignAgentMutation = useMutation(
    (agentId) => ticketService.assignTicket(id, agentId),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['ticket', id]);
        setAssignDialog(false);
        setSelectedAgent('');
        toast.success('Ticket assigned successfully');
      },
      onError: () => toast.error('Failed to assign ticket'),
    }
  );

  // Determine what statuses this user can transition to from current
  const getValidNextStatuses = (current) => {
    const isAdmin = ['Mission_Admin', 'HQ_Super_Admin'].includes(user?.role);
    if (isAdmin) return ['Open', 'Assigned', 'In_Progress', 'Resolved', 'Closed'];
    // Agents can move forward only
    const forward = {
      Open: ['Assigned', 'In_Progress'],
      Assigned: ['In_Progress', 'Resolved'],
      In_Progress: ['Resolved'],
      Resolved: ['Closed'],
      Closed: [],
    };
    return forward[current] || [];
  };

  const canChangeStatus = user?.role !== 'Requester';
  const canEscalate = ['Agent', 'Mission_Admin', 'HQ_Super_Admin'].includes(user?.role);
  const canAddInternal = user?.role !== 'Requester';
  // Compare as strings to handle MongoDB ObjectId types
  const canAssignToMe = ['Agent', 'Mission_Admin', 'HQ_Super_Admin'].includes(user?.role)
    && ticket?.status !== 'Resolved'
    && ticket?.status !== 'Closed'
    && String(ticket?.assigned_agent ?? '') !== String(user?.id ?? 'x');
  const canAssignAgent = isAdmin
    && ticket?.status !== 'Resolved'
    && ticket?.status !== 'Closed';

  if (isLoading) return <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}><CircularProgress /></Box>;
  if (error) return <Alert severity="error">Error loading ticket: {error.message}</Alert>;
  if (!ticket) return <Alert severity="warning">Ticket not found</Alert>;

  return (
    <Box>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 3, gap: 2 }}>
        <Button startIcon={<ArrowBack />} onClick={() => navigate('/tickets')}>
          Back to Tickets
        </Button>
        <Typography variant="h5" sx={{ flexGrow: 1 }}>
          {ticket.ticket_number} — {ticket.title}
        </Typography>
      {canChangeStatus && (
          <Button variant="outlined" onClick={() => { setNewStatus(ticket.status); setNewStatusComment(''); setStatusDialog(true); }}>
            Update Status
          </Button>
        )}
        {canAssignAgent && (
          <Button
            variant="outlined"
            color="primary"
            startIcon={<AssignmentInd />}
            onClick={() => { setSelectedAgent(ticket.assigned_agent || ''); setAssignDialog(true); }}
          >
            Assign Agent
          </Button>
        )}
        {canAssignToMe && (
          <Button
            variant="outlined"
            color="success"
            startIcon={<PersonAdd />}
            onClick={() => assignToMeMutation.mutate()}
            disabled={assignToMeMutation.isLoading}
          >
            Assign to Me
          </Button>
        )}
        {canEscalate && !ticket.escalated_to_hq && (
          <Button variant="outlined" color="warning" startIcon={<Escalator />} onClick={() => setEscalateDialog(true)}>
            Escalate to HQ
          </Button>
        )}
      </Box>

      <Grid container spacing={3}>
        {/* Main ticket info */}
        <Grid item xs={12} md={8}>
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>Description</Typography>
              <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>{ticket.description}</Typography>
            </CardContent>
          </Card>

          {/* Comments */}
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>Activity</Typography>
              <Divider sx={{ mb: 2 }} />
              {ticket.comments?.length === 0 && (
                <Typography color="text.secondary" sx={{ mb: 2 }}>No comments yet.</Typography>
              )}
              {ticket.comments?.map((c) => (
                <Box key={c.id} sx={{ mb: 2, p: 2, bgcolor: c.is_internal ? 'warning.50' : 'grey.50', borderRadius: 1, border: c.is_internal ? '1px dashed orange' : 'none' }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                    <Avatar sx={{ width: 28, height: 28, fontSize: 12 }}>{c.author_name?.charAt(0)}</Avatar>
                    <Typography variant="subtitle2">{c.author_name}</Typography>
                    <Typography variant="caption" color="text.secondary">
                      {new Date(c.created_at).toLocaleString()}
                    </Typography>
                    {c.is_internal && <Chip label="Internal" size="small" color="warning" />}
                  </Box>
                  <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>{c.content}</Typography>
                </Box>
              ))}

              <Divider sx={{ my: 2 }} />
              <Typography variant="subtitle1" gutterBottom>Add Comment</Typography>
              <TextField
                fullWidth
                multiline
                rows={3}
                placeholder="Write a comment..."
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                sx={{ mb: 1 }}
              />
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                {canAddInternal && (
                  <FormControlLabel
                    control={<Switch checked={isInternal} onChange={(e) => setIsInternal(e.target.checked)} />}
                    label="Internal note (not visible to requester)"
                  />
                )}
                <Button
                  variant="contained"
                  startIcon={<Send />}
                  onClick={() => addCommentMutation.mutate({ content: comment, isInternal })}
                  disabled={!comment.trim() || addCommentMutation.isLoading}
                >
                  Submit
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Sidebar info */}
        <Grid item xs={12} md={4}>
          <Card sx={{ mb: 2 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>Details</Typography>
              <Stack spacing={1.5}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                  <Typography variant="body2" color="text.secondary">Status</Typography>
                  <Chip label={ticket.status?.replace('_', ' ')} color={STATUS_COLORS[ticket.status]} size="small" />
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                  <Typography variant="body2" color="text.secondary">Priority</Typography>
                  <Chip label={ticket.priority} color={PRIORITY_COLORS[ticket.priority]} size="small" />
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                  <Typography variant="body2" color="text.secondary">Category</Typography>
                  <Typography variant="body2">{ticket.category_name}</Typography>
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                  <Typography variant="body2" color="text.secondary">Mission</Typography>
                  <Typography variant="body2">{ticket.mission_name}</Typography>
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                  <Typography variant="body2" color="text.secondary">Dept From</Typography>
                  <Typography variant="body2">{ticket.department_from || 'N/A'}</Typography>
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                  <Typography variant="body2" color="text.secondary">Dept To</Typography>
                  <Typography variant="body2">{ticket.department_to || 'N/A'}</Typography>
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                  <Typography variant="body2" color="text.secondary">Room</Typography>
                  <Typography variant="body2">{ticket.room_number || 'N/A'}</Typography>
                </Box>
                <Divider />
                <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                  <Typography variant="body2" color="text.secondary">Submitted By</Typography>
                  <Typography variant="body2" align="right" sx={{ maxWidth: 160 }}>{ticket.submission_display}</Typography>
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                  <Typography variant="body2" color="text.secondary">Assigned To</Typography>
                  <Typography variant="body2">{ticket.agent_name || <span style={{ color: '#9e9e9e' }}>Unassigned</span>}</Typography>
                </Box>
                <Divider />
                <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                  <Typography variant="body2" color="text.secondary">Created</Typography>
                  <Typography variant="body2">{new Date(ticket.created_at).toLocaleDateString()}</Typography>
                </Box>
                {ticket.sla_due_date && (
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography variant="body2" color="text.secondary">SLA Due</Typography>
                    <Typography variant="body2" color={ticket.is_overdue ? 'error' : 'inherit'}>
                      {new Date(ticket.sla_due_date).toLocaleDateString()}
                    </Typography>
                  </Box>
                )}
                {ticket.escalated_to_hq && (
                  <Chip label="Escalated to HQ" color="warning" size="small" />
                )}
              </Stack>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Status Update Dialog */}
      <Dialog open={statusDialog} onClose={() => setStatusDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Update Ticket Status</DialogTitle>
        <DialogContent>
          <FormControl fullWidth sx={{ mt: 1, mb: 2 }}>
            <InputLabel>New Status</InputLabel>
            <Select value={newStatus} label="New Status" onChange={(e) => setNewStatus(e.target.value)}>
              {getValidNextStatuses(ticket?.status).map(s => (
                <MenuItem key={s} value={s}>{s.replace('_', ' ')}</MenuItem>
              ))}
            </Select>
          </FormControl>
          <TextField
            fullWidth
            multiline
            rows={2}
            label="Comment (optional)"
            value={newStatusComment}
            onChange={(e) => setNewStatusComment(e.target.value)}
            placeholder="Add a note about this status change..."
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setStatusDialog(false)}>Cancel</Button>
          <Button
            variant="contained"
            onClick={() => updateStatusMutation.mutate({ status: newStatus, comment: newStatusComment })}
            disabled={!newStatus || updateStatusMutation.isLoading}
          >
            Update
          </Button>
        </DialogActions>
      </Dialog>

      {/* Escalate Dialog */}
      <Dialog open={escalateDialog} onClose={() => setEscalateDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Escalate Ticket to HQ</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            multiline
            rows={3}
            label="Reason for escalation"
            value={escalateReason}
            onChange={(e) => setEscalateReason(e.target.value)}
            sx={{ mt: 1 }}
            required
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEscalateDialog(false)}>Cancel</Button>
          <Button
            variant="contained"
            color="warning"
            onClick={() => escalateMutation.mutate(escalateReason)}
            disabled={!escalateReason.trim() || escalateMutation.isLoading}
          >
            Escalate
          </Button>
        </DialogActions>
      </Dialog>
      {/* Assign Agent Dialog */}
      <Dialog open={assignDialog} onClose={() => setAssignDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Assign Ticket to Agent</DialogTitle>
        <DialogContent>
          <FormControl fullWidth sx={{ mt: 1 }}>
            <InputLabel>Select Agent / Admin</InputLabel>
            <Select
              value={selectedAgent}
              label="Select Agent / Admin"
              onChange={(e) => setSelectedAgent(e.target.value)}
            >
              <MenuItem value="">— Unassign —</MenuItem>
              {agentsList.map((a) => (
                <MenuItem key={a.id} value={a.id}>
                  {a.full_name || `${a.first_name} ${a.last_name}`}
                  <Typography variant="caption" color="text.secondary" sx={{ ml: 1 }}>
                    ({a.role?.replace('_', ' ')} · {a.department || 'No dept'})
                  </Typography>
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAssignDialog(false)}>Cancel</Button>
          <Button
            variant="contained"
            onClick={() => assignAgentMutation.mutate(selectedAgent || null)}
            disabled={assignAgentMutation.isLoading}
          >
            Assign
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default TicketDetail;
