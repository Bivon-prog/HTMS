import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  Alert,
  Container,
  CircularProgress,
} from '@mui/material';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import authService from '../../services/authService';

const Login = ({ onLogin }) => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const onSubmit = async (data) => {
    setLoading(true);
    setError('');
    
    try {
      await authService.login(data.email, data.password);
      toast.success('Login successful!');
      if (onLogin) onLogin();
      navigate('/dashboard');
    } catch (err) {
      const errorMessage = err.response?.data?.non_field_errors?.[0] 
        || err.response?.data?.error 
        || 'Login failed. Please try again.';
      setError(errorMessage);
      toast.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container component="main" maxWidth="sm">
      <Box
        sx={{
          minHeight: '100vh',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
        }}
      >
        <Card sx={{ width: '100%', maxWidth: 400 }}>
          <CardContent sx={{ p: 4 }}>
            <Box sx={{ textAlign: 'center', mb: 3 }}>
              <Typography component="h1" variant="h4" color="primary" gutterBottom>
                HTMS
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Helpdesk Ticket Management System
              </Typography>
              <Typography variant="caption" color="text.secondary" display="block" sx={{ mt: 1 }}>
                Ministry of Foreign and Diaspora Affairs, Kenya
              </Typography>
            </Box>

            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}

            <form onSubmit={handleSubmit(onSubmit)}>
              <TextField
                {...register('email', {
                  required: 'Email is required',
                  pattern: {
                    value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                    message: 'Invalid email address',
                  },
                })}
                fullWidth
                label="Email Address"
                type="email"
                margin="normal"
                error={!!errors.email}
                helperText={errors.email?.message}
                disabled={loading}
              />

              <TextField
                {...register('password', {
                  required: 'Password is required',
                })}
                fullWidth
                label="Password"
                type="password"
                margin="normal"
                error={!!errors.password}
                helperText={errors.password?.message}
                disabled={loading}
              />

              <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
                disabled={loading}
              >
                {loading ? <CircularProgress size={24} /> : 'Sign In'}
              </Button>
            </form>

            <Box sx={{ textAlign: 'center', mt: 2 }}>
              <Button
                variant="text"
                size="small"
                onClick={() => {/* TODO: Implement password reset */}}
                disabled={loading}
              >
                Forgot Password?
              </Button>
            </Box>
          </CardContent>
        </Card>
      </Box>
    </Container>
  );
};

export default Login;
