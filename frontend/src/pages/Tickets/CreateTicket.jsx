import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box, Card, CardContent, Typography, TextField, Button,
  MenuItem, Select, FormControl, InputLabel, Alert,
  CircularProgress, Grid, FormHelperText,
} from '@mui/material';
import { ArrowBack, Send } from '@mui/icons-material';
import { useForm, Controller } from 'react-hook-form';
import { useQuery, useMutation } from 'react-query';
import toast from 'react-hot-toast';
import ticketService from '../../services/ticketService';
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({ baseURL: API_BASE_URL });
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

const CreateTicket = () => {
  const navigate = useNavigate();
  const [attachments, setAttachments] = useState([]);

  const { data: categories = [] } = useQuery('categories', async () => {
    const res = await api.get('/missions/categories/');
    return res.data.results || res.data;
  });

  const { data: assets = [] } = useQuery('assets-search', async () => {
    const res = await api.get('/assets/');
    return res.data.results || res.data;
  });

  const {
    register, handleSubmit, control,
    formState: { errors },
  } = useForm({
    defaultValues: { priority: 'Medium' },
  });

  const { data: oboGrants = [] } = useQuery('obo-grants', async () => {
    const res = await api.get('/auth/on-behalf-grants/');
    return res.data.results || res.data;
  });

  const createMutation = useMutation(
    (data) => ticketService.createTicket(data),
    {
      onSuccess: async (data) => {
        // Upload attachments sequentially if there are any
        for (const file of attachments) {
          try {
            await ticketService.uploadAttachment(data.id, file);
          } catch (err) {
            toast.error(`Failed to upload ${file.name}`);
          }
        }
        toast.success(`Ticket ${data.ticket_number} created successfully`);
        navigate('/tickets');
      },
      onError: (err) => {
        const msg = err.response?.data?.detail || 'Failed to create ticket';
        toast.error(msg);
      },
    }
  );

  const onSubmit = (data) => {
    const payload = {
      title: data.title,
      description: data.description,
      category: data.category,
      priority: data.priority,
    };
    if (data.linked_asset) payload.linked_asset = data.linked_asset;
    if (data.beneficiary) payload.beneficiary = data.beneficiary;
    createMutation.mutate(payload);
  };

  const handleFileChange = (e) => {
    const files = Array.from(e.target.files);
    const allowed = ['application/pdf', 'image/jpeg', 'image/png',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    const valid = files.filter(f => {
      if (!allowed.includes(f.type)) { toast.error(`${f.name}: unsupported file type`); return false; }
      if (f.size > 10 * 1024 * 1024) { toast.error(`${f.name}: exceeds 10MB limit`); return false; }
      return true;
    });
    setAttachments(prev => [...prev, ...valid].slice(0, 5));
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 3, gap: 2 }}>
        <Button startIcon={<ArrowBack />} onClick={() => navigate('/tickets')}>
          Back
        </Button>
        <Typography variant="h5">Create New Ticket</Typography>
      </Box>

      <Card sx={{ maxWidth: 800 }}>
        <CardContent>
          <form onSubmit={handleSubmit(onSubmit)}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <TextField
                  {...register('title', { required: 'Title is required', maxLength: { value: 255, message: 'Max 255 characters' } })}
                  fullWidth
                  label="Title"
                  error={!!errors.title}
                  helperText={errors.title?.message}
                />
              </Grid>

              <Grid item xs={12}>
                <TextField
                  {...register('description', { required: 'Description is required' })}
                  fullWidth
                  multiline
                  rows={5}
                  label="Description"
                  error={!!errors.description}
                  helperText={errors.description?.message}
                />
              </Grid>

              <Grid item xs={12} sm={6}>
                <FormControl fullWidth error={!!errors.category}>
                  <InputLabel>Category *</InputLabel>
                  <Controller
                    name="category"
                    control={control}
                    defaultValue=""
                    rules={{ required: 'Category is required' }}
                    render={({ field }) => (
                      <Select {...field} label="Category *">
                        {categories.map((cat) => (
                          <MenuItem key={cat.id} value={cat.id}>{cat.name}</MenuItem>
                        ))}
                      </Select>
                    )}
                  />
                  {errors.category && <FormHelperText>{errors.category.message}</FormHelperText>}
                </FormControl>
              </Grid>

              <Grid item xs={12} sm={6}>
                <FormControl fullWidth>
                  <InputLabel>Priority</InputLabel>
                  <Controller
                    name="priority"
                    control={control}
                    render={({ field }) => (
                      <Select {...field} label="Priority">
                        <MenuItem value="Low">Low</MenuItem>
                        <MenuItem value="Medium">Medium</MenuItem>
                        <MenuItem value="High">High</MenuItem>
                        <MenuItem value="Critical">Critical</MenuItem>
                      </Select>
                    )}
                  />
                </FormControl>
              </Grid>

              <Grid item xs={12}>
                <FormControl fullWidth>
                  <InputLabel>Link Asset (optional)</InputLabel>
                  <Controller
                    name="linked_asset"
                    control={control}
                    render={({ field }) => (
                      <Select {...field} label="Link Asset (optional)">
                        <MenuItem value="">None</MenuItem>
                        {assets.map((a) => (
                          <MenuItem key={a.id} value={a.id}>
                            {a.inventory_tag} — {a.device_type} {a.make} {a.model}
                          </MenuItem>
                        ))}
                      </Select>
                    )}
                  />
                </FormControl>
              </Grid>

              {oboGrants.length > 0 && (
                <Grid item xs={12}>
                  <FormControl fullWidth>
                    <InputLabel>Submit On Behalf Of (optional)</InputLabel>
                    <Controller
                      name="beneficiary"
                      control={control}
                      defaultValue=""
                      render={({ field }) => (
                        <Select {...field} label="Submit On Behalf Of (optional)">
                          <MenuItem value="">Myself</MenuItem>
                          {oboGrants.map((grant) => (
                            <MenuItem key={grant.id} value={grant.official}>
                              {grant.official_name}
                            </MenuItem>
                          ))}
                        </Select>
                      )}
                    />
                  </FormControl>
                </Grid>
              )}

              <Grid item xs={12}>
                <Button variant="outlined" component="label" startIcon={<Send />}>
                  Attach Files (PDF, JPEG, PNG, DOCX — max 10MB each, up to 5)
                  <input type="file" hidden multiple accept=".pdf,.jpg,.jpeg,.png,.docx" onChange={handleFileChange} />
                </Button>
                {attachments.length > 0 && (
                  <Box sx={{ mt: 1 }}>
                    {attachments.map((f, i) => (
                      <Typography key={i} variant="caption" display="block" color="text.secondary">
                        {f.name} ({(f.size / 1024).toFixed(1)} KB)
                      </Typography>
                    ))}
                  </Box>
                )}
              </Grid>

              <Grid item xs={12}>
                <Box sx={{ display: 'flex', gap: 2 }}>
                  <Button
                    type="submit"
                    variant="contained"
                    disabled={createMutation.isLoading}
                    startIcon={createMutation.isLoading ? <CircularProgress size={16} /> : <Send />}
                  >
                    Submit Ticket
                  </Button>
                  <Button variant="outlined" onClick={() => navigate('/tickets')}>
                    Cancel
                  </Button>
                </Box>
              </Grid>
            </Grid>
          </form>
        </CardContent>
      </Card>
    </Box>
  );
};

export default CreateTicket;
