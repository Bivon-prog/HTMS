import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  Drawer, List, ListItem, ListItemButton, ListItemIcon, ListItemText,
  Toolbar, Divider, Collapse, Box, Typography, Chip, Avatar,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  SupportAgent as TicketIcon,
  Add as CreateTicketIcon,
  Inventory as AssetIcon,
  People as UserIcon,
  LocationOn as MissionIcon,
  ExpandLess, ExpandMore,
  BarChart as ReportIcon,
  AssignmentInd as MyQueueIcon,
  Inbox as OpenQueueIcon,
} from '@mui/icons-material';
import authService from '../../services/authService';

const DRAWER_WIDTH = 240;

const ROLE_LABELS = {
  Requester: 'Requester',
  Agent: 'Agent',
  Mission_Admin: 'Mission Admin',
  HQ_Super_Admin: 'HQ Super Admin',
};

const ROLE_COLORS = {
  Requester: 'default',
  Agent: 'primary',
  Mission_Admin: 'warning',
  HQ_Super_Admin: 'error',
};

const Sidebar = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [openTickets, setOpenTickets] = useState(true);
  const user = authService.getCurrentUser() || {};
  const role = user.role || '';

  const isAgent = ['Agent', 'Mission_Admin', 'HQ_Super_Admin'].includes(role);
  const isAdmin = ['Mission_Admin', 'HQ_Super_Admin'].includes(role);
  const isHQ = role === 'HQ_Super_Admin';

  const isActive = (path) => location.pathname === path;
  const isActiveQuery = (path, q) =>
    location.pathname === path && location.search.includes(q);

  const go = (path) => navigate(path);

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: DRAWER_WIDTH,
        flexShrink: 0,
        [`& .MuiDrawer-paper`]: {
          width: DRAWER_WIDTH,
          boxSizing: 'border-box',
          display: 'flex',
          flexDirection: 'column',
        },
      }}
    >
      <Toolbar />
      <Box sx={{ flexGrow: 1, overflow: 'auto' }}>
        <List dense>

          {/* Dashboard */}
          <ListItem disablePadding>
            <ListItemButton selected={isActive('/dashboard')} onClick={() => go('/dashboard')}>
              <ListItemIcon><DashboardIcon fontSize="small" /></ListItemIcon>
              <ListItemText primary="Dashboard" />
            </ListItemButton>
          </ListItem>

          {/* Tickets — collapsible */}
          <ListItem disablePadding>
            <ListItemButton onClick={() => setOpenTickets(o => !o)}>
              <ListItemIcon><TicketIcon fontSize="small" /></ListItemIcon>
              <ListItemText primary="Tickets" />
              {openTickets ? <ExpandLess fontSize="small" /> : <ExpandMore fontSize="small" />}
            </ListItemButton>
          </ListItem>
          <Collapse in={openTickets} timeout="auto" unmountOnExit>
            <List component="div" disablePadding dense>

              {/* All Tickets */}
              <ListItem disablePadding>
                <ListItemButton
                  sx={{ pl: 4 }}
                  selected={isActive('/tickets') && !location.search}
                  onClick={() => go('/tickets')}
                >
                  <ListItemIcon><TicketIcon fontSize="small" /></ListItemIcon>
                  <ListItemText primary="All Tickets" />
                </ListItemButton>
              </ListItem>

              {/* My Queue — agents & admins */}
              {isAgent && (
                <ListItem disablePadding>
                  <ListItemButton
                    sx={{ pl: 4 }}
                    selected={isActiveQuery('/tickets', 'queue=mine')}
                    onClick={() => go('/tickets?queue=mine')}
                  >
                    <ListItemIcon><MyQueueIcon fontSize="small" /></ListItemIcon>
                    <ListItemText primary="My Queue" />
                  </ListItemButton>
                </ListItem>
              )}

              {/* Open Queue — agents & admins */}
              {isAgent && (
                <ListItem disablePadding>
                  <ListItemButton
                    sx={{ pl: 4 }}
                    selected={isActiveQuery('/tickets', 'queue=open')}
                    onClick={() => go('/tickets?queue=open')}
                  >
                    <ListItemIcon><OpenQueueIcon fontSize="small" /></ListItemIcon>
                    <ListItemText primary="Open Queue" />
                  </ListItemButton>
                </ListItem>
              )}

              {/* Create Ticket */}
              <ListItem disablePadding>
                <ListItemButton
                  sx={{ pl: 4 }}
                  selected={isActive('/tickets/create')}
                  onClick={() => go('/tickets/create')}
                >
                  <ListItemIcon><CreateTicketIcon fontSize="small" /></ListItemIcon>
                  <ListItemText primary="Create Ticket" />
                </ListItemButton>
              </ListItem>

            </List>
          </Collapse>

          {/* Assets */}
          <ListItem disablePadding>
            <ListItemButton selected={isActive('/assets')} onClick={() => go('/assets')}>
              <ListItemIcon><AssetIcon fontSize="small" /></ListItemIcon>
              <ListItemText primary="Assets" />
            </ListItemButton>
          </ListItem>

          {/* Users — admins only */}
          {isAdmin && (
            <ListItem disablePadding>
              <ListItemButton selected={isActive('/users')} onClick={() => go('/users')}>
                <ListItemIcon><UserIcon fontSize="small" /></ListItemIcon>
                <ListItemText primary="Users" />
              </ListItemButton>
            </ListItem>
          )}

          {/* Missions — HQ only */}
          {isHQ && (
            <ListItem disablePadding>
              <ListItemButton selected={isActive('/missions')} onClick={() => go('/missions')}>
                <ListItemIcon><MissionIcon fontSize="small" /></ListItemIcon>
                <ListItemText primary="Missions" />
              </ListItemButton>
            </ListItem>
          )}

        </List>

        <Divider />

        <List dense>
          <ListItem disablePadding>
            <ListItemButton disabled>
              <ListItemIcon><ReportIcon fontSize="small" /></ListItemIcon>
              <ListItemText primary="Reports" secondary="Coming soon" />
            </ListItemButton>
          </ListItem>
        </List>
      </Box>

      {/* User role footer */}
      <Divider />
      <Box sx={{ p: 1.5, display: 'flex', alignItems: 'center', gap: 1.5 }}>
        <Avatar sx={{ width: 32, height: 32, bgcolor: 'primary.main', fontSize: 14 }}>
          {user.first_name?.charAt(0) || 'U'}
        </Avatar>
        <Box sx={{ minWidth: 0 }}>
          <Typography variant="caption" fontWeight={600} noWrap display="block">
            {user.first_name} {user.last_name}
          </Typography>
          <Chip
            label={ROLE_LABELS[role] || role}
            color={ROLE_COLORS[role] || 'default'}
            size="small"
            sx={{ height: 16, fontSize: 10 }}
          />
        </Box>
      </Box>
    </Drawer>
  );
};

export default Sidebar;
