import React, { useState } from 'react';
import {
  Box, Card, CardContent, Typography, TextField, Button,
  Grid, Alert, CircularProgress, Divider, Avatar, Chip,
} from '@mui/material';
import { useForm } from 'react-hook-form';
import { useMutation } from 'react-query';
import toast from 'react-hot-toast';
import authService from '../../services/authService';

const ROLE_COLORS = {
  Requester: 'default', Agent: 'info',
  Mission_Admin: 'warning', HQ_Super_Admin: 'error',
};

const Profile = () => {
  const user = authService.getCurrentUser();
  const [profileSuccess, setProfileSuccess] = useState(false);
  const [passwordSuccess, setPasswordSuccess] = useState(false);

  const { register: regProfile, handleSubmit: handleProfile, formState: { errors: profileErrors } } = useForm({
    defaultValues: { first_name: user?.first_name || '', last_name: user?.last_name || '' },
  });

  const { register: regPwd, handleSubmit: handlePwd, formState: { errors: pwdErrors }, reset: resetPwd, watch } = useForm();
  const newPassword = watch('new_password');

  const profileMutation = useMutation(
    (data) => authService.updateProfile(data),
    {
      onSuccess: () => { setProfileSuccess(true); toast.success('Profile updated'); },
      onError: () => toast.error('Failed to update profile'),
    }
  );

  const passwordMutation = useMutation(
    (data) => authService.updateProfile(data),
    {
      onSuccess: () => { setPasswordSuccess(true); resetPwd(); toast.success('Password changed'); },
      onError: (err) => {
        const msg = err.response?.data?.non_field_errors?.[0] || 'Failed to change password';
        toast.error(msg);
      },
    }
  );

  return (
    <Box sx={{ maxWidth: 800 }}>
      <Typography variant="h4" gutterBottom>My Profile</Typography>

      {/* User info card */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
            <Avatar sx={{ width: 64, height: 64, fontSize: 24, bgcolor: 'primary.main' }}>
              {user?.first_name?.charAt(0)}{user?.last_name?.charAt(0)}
            </Avatar>
            <Box>
              <Typography variant="h6">{user?.first_name} {user?.last_name}</Typography>
              <Typography variant="body2" color="text.secondary">{user?.email}</Typography>
              <Box sx={{ display: 'flex', gap: 1, mt: 0.5 }}>
                {user?.user_id && <Chip label={`ID: ${user.user_id}`} size="small" color="primary" variant="outlined" />}
                <Chip label={user?.role?.replace('_', ' ')} color={ROLE_COLORS[user?.role] || 'default'} size="small" />
                {user?.department && <Chip label={user.department} size="small" variant="outlined" />}
                {user?.mission_name && <Chip label={user.mission_name} size="small" variant="outlined" />}
              </Box>
            </Box>
          </Box>
        </CardContent>
      </Card>

      {/* Edit profile */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>Edit Profile</Typography>
          {profileSuccess && <Alert severity="success" sx={{ mb: 2 }}>Profile updated successfully</Alert>}
          <form onSubmit={handleProfile((d) => profileMutation.mutate(d))}>
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <TextField {...regProfile('first_name', { required: 'Required' })} fullWidth label="First Name"
                  error={!!profileErrors.first_name} helperText={profileErrors.first_name?.message} />
              </Grid>
              <Grid item xs={6}>
                <TextField {...regProfile('last_name', { required: 'Required' })} fullWidth label="Last Name"
                  error={!!profileErrors.last_name} helperText={profileErrors.last_name?.message} />
              </Grid>
              <Grid item xs={12}>
                <Button type="submit" variant="contained" disabled={profileMutation.isLoading}>
                  {profileMutation.isLoading ? <CircularProgress size={20} /> : 'Save Changes'}
                </Button>
              </Grid>
            </Grid>
          </form>
        </CardContent>
      </Card>

      {/* Change password */}
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>Change Password</Typography>
          {passwordSuccess && <Alert severity="success" sx={{ mb: 2 }}>Password changed successfully</Alert>}
          <form onSubmit={handlePwd((d) => passwordMutation.mutate(d))}>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <TextField {...regPwd('current_password', { required: 'Required' })} fullWidth
                  label="Current Password" type="password"
                  error={!!pwdErrors.current_password} helperText={pwdErrors.current_password?.message} />
              </Grid>
              <Grid item xs={12}>
                <TextField {...regPwd('new_password', { required: 'Required', minLength: { value: 8, message: 'Min 8 characters' } })}
                  fullWidth label="New Password" type="password"
                  error={!!pwdErrors.new_password} helperText={pwdErrors.new_password?.message} />
              </Grid>
              <Grid item xs={12}>
                <TextField {...regPwd('new_password_confirm', {
                  required: 'Required',
                  validate: (v) => v === newPassword || 'Passwords do not match',
                })} fullWidth label="Confirm New Password" type="password"
                  error={!!pwdErrors.new_password_confirm} helperText={pwdErrors.new_password_confirm?.message} />
              </Grid>
              <Grid item xs={12}>
                <Button type="submit" variant="contained" disabled={passwordMutation.isLoading}>
                  {passwordMutation.isLoading ? <CircularProgress size={20} /> : 'Change Password'}
                </Button>
              </Grid>
            </Grid>
          </form>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Profile;
