import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
  Divider,
  Collapse,
  Box,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  SupportAgent as TicketIcon,
  Add as CreateTicketIcon,
  Inventory as AssetIcon,
  People as UserIcon,
  LocationOn as MissionIcon,
  ExpandLess,
  ExpandMore,
  BarChart as ReportIcon,
} from '@mui/icons-material';

const drawerWidth = 240;

const menuItems = [
  {
    text: 'Dashboard',
    icon: <DashboardIcon />,
    path: '/dashboard',
  },
  {
    text: 'Tickets',
    icon: <TicketIcon />,
    children: [
      {
        text: 'All Tickets',
        icon: <TicketIcon />,
        path: '/tickets',
      },
      {
        text: 'Create Ticket',
        icon: <CreateTicketIcon />,
        path: '/tickets/create',
      },
    ],
  },
  {
    text: 'Assets',
    icon: <AssetIcon />,
    path: '/assets',
  },
  {
    text: 'Users',
    icon: <UserIcon />,
    path: '/users',
    role: ['Mission_Admin', 'HQ_Super_Admin'],
  },
  {
    text: 'Missions',
    icon: <MissionIcon />,
    path: '/missions',
    role: ['HQ_Super_Admin'],
  },
];

const Sidebar = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [openTickets, setOpenTickets] = useState(false);
  const user = JSON.parse(localStorage.getItem('user') || '{}');

  const handleNavigation = (path) => {
    navigate(path);
  };

  const toggleTicketsMenu = () => {
    setOpenTickets(!openTickets);
  };

  const isMenuItemActive = (path) => {
    return location.pathname === path;
  };

  const isMenuParentActive = (children) => {
    return children?.some(child => location.pathname === child.path);
  };

  const canAccessMenuItem = (item) => {
    if (!item.role) return true;
    return item.role.includes(user.role);
  };

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
      }}
    >
      <Toolbar />
      <Box sx={{ overflow: 'auto' }}>
        <List>
          {menuItems.map((item) => {
            if (!canAccessMenuItem(item)) return null;

            if (item.children) {
              const isActive = isMenuParentActive(item.children);
              return (
                <React.Fragment key={item.text}>
                  <ListItem disablePadding>
                    <ListItemButton
                      onClick={toggleTicketsMenu}
                      selected={isActive}
                    >
                      <ListItemIcon>{item.icon}</ListItemIcon>
                      <ListItemText primary={item.text} />
                      {openTickets ? <ExpandLess /> : <ExpandMore />}
                    </ListItemButton>
                  </ListItem>
                  <Collapse in={openTickets || isActive} timeout="auto" unmountOnExit>
                    <List component="div" disablePadding>
                      {item.children.map((child) => (
                        <ListItem key={child.text} disablePadding>
                          <ListItemButton
                            sx={{ pl: 4 }}
                            selected={isMenuItemActive(child.path)}
                            onClick={() => handleNavigation(child.path)}
                          >
                            <ListItemIcon>{child.icon}</ListItemIcon>
                            <ListItemText primary={child.text} />
                          </ListItemButton>
                        </ListItem>
                      ))}
                    </List>
                  </Collapse>
                </React.Fragment>
              );
            }

            return (
              <ListItem key={item.text} disablePadding>
                <ListItemButton
                  selected={isMenuItemActive(item.path)}
                  onClick={() => handleNavigation(item.path)}
                >
                  <ListItemIcon>{item.icon}</ListItemIcon>
                  <ListItemText primary={item.text} />
                </ListItemButton>
              </ListItem>
            );
          })}
        </List>
        <Divider />
        <List>
          <ListItem disablePadding>
            <ListItemButton>
              <ListItemIcon>
                <ReportIcon />
              </ListItemIcon>
              <ListItemText primary="Reports" />
            </ListItemButton>
          </ListItem>
        </List>
      </Box>
    </Drawer>
  );
};

export default Sidebar;
