# HTMS — Quick Start Guide (Supabase Development)

Complete setup guide for the Helpdesk Ticket Management System using Supabase as the development database.

---

## Prerequisites

- **Python 3.8+** installed
- **Node.js 16+** and npm installed
- **Supabase account** with a project created
- **Git** (optional, for version control)

---

## Step 1: Clone & Setup Environment

```bash
# Navigate to project directory
cd HTMS

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

---

## Step 2: Configure Supabase Connection

Your `.env.supabase` file should already contain your Supabase credentials:

```env
# Supabase Database Configuration
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=your_supabase_password
SUPABASE_DB_HOST=your_project.supabase.co
SUPABASE_DB_PORT=5432
```

**✅ These are already configured in your `.env.supabase` file.**

---

## Step 3: Run Complete Setup

Run the automated setup script:

```bash
python setup_complete.py
```

This script will:
1. ✅ Test database connection
2. ✅ Create all database migrations
3. ✅ Apply migrations to Supabase
4. ✅ Load all 70 missions
5. ✅ Load ticket categories (IT, HR, Facilities, etc.)
6. ✅ Create HQ Super Admin user
7. ✅ Collect static files

**Follow the prompts to create your admin account.**

---

## Step 4: Start Backend Server

```bash
python manage_supabase.py runserver
```

The backend API will be available at: **http://localhost:8000**

Test it: http://localhost:8000/api/health/

---

## Step 5: Setup Frontend

Open a **new terminal** (keep backend running):

```bash
cd frontend

# Install dependencies (first time only)
npm install

# Start development server
npm start
```

The frontend will open automatically at: **http://localhost:3000**

---

## Step 6: Login & Test

1. Open **http://localhost:3000**
2. Login with the credentials you created during setup
3. You should see the dashboard with all 70 missions loaded

---

## Default Admin Credentials

If you used the defaults during setup:

- **Email:** `admin@htms.go.ke`
- **Password:** `admin123`

**⚠️ Change this password in production!**

---

## Verify Setup

### Check Missions Loaded

```bash
python manage_supabase.py shell
```

```python
from apps.missions.models import Mission
print(f"Missions loaded: {Mission.objects.count()}")  # Should be 70
Mission.objects.values_list('name', 'country')[:5]
```

### Check Categories Loaded

```python
from apps.missions.models import TicketCategory
TicketCategory.objects.values_list('name', 'auto_escalation_hours')
```

---

## Common Issues & Solutions

### Issue: Database Connection Failed

**Solution:** Check your `.env.supabase` file:
- Ensure `SUPABASE_DB_HOST` is correct (e.g., `kdcacxkohwhvlzyszlzv.supabase.co`)
- Verify `SUPABASE_DB_PASSWORD` is correct
- Check Supabase dashboard → Settings → Database → Connection string

### Issue: Port 8000 Already in Use

**Solution:**
```bash
# Use a different port
python manage_supabase.py runserver 8001
```

Then update frontend `.env`:
```
REACT_APP_API_URL=http://localhost:8001/api
```

### Issue: Frontend Can't Connect to Backend

**Solution:**
1. Ensure backend is running on port 8000
2. Check `frontend/.env` has: `REACT_APP_API_URL=http://localhost:8000/api`
3. Check browser console for CORS errors

### Issue: Migrations Already Applied

**Solution:** This is normal if you've run setup before. The script skips existing migrations.

---

## Project Structure

```
HTMS/
├── apps/                      # Django apps
│   ├── authentication/        # User auth & JWT
│   ├── tickets/              # Ticket management
│   ├── missions/             # 70 missions + categories
│   ├── assets/               # Asset tracking
│   ├── notifications/        # Notification system
│   ├── dashboard/            # Analytics & reports
│   └── users/                # User management
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── pages/           # All UI pages
│   │   ├── components/      # Reusable components
│   │   └── services/        # API services
│   └── package.json
├── htms/                     # Django project settings
│   ├── settings.py          # Main settings
│   └── settings_supabase.py # Supabase config
├── manage_supabase.py       # Django management (Supabase)
├── setup_complete.py        # Automated setup script
└── requirements.txt         # Python dependencies
```

---

## Available Management Commands

```bash
# Load/reload missions
python manage_supabase.py load_missions

# Clear and reload missions
python manage_supabase.py load_missions --clear

# Create additional superuser
python manage_supabase.py createsuperuser

# Django shell
python manage_supabase.py shell

# Run tests
python manage_supabase.py test
```

---

## API Endpoints

### Authentication
- `POST /api/auth/login/` — Login
- `POST /api/auth/logout/` — Logout
- `POST /api/auth/refresh/` — Refresh JWT token
- `GET /api/auth/verify/` — Verify token
- `GET /api/auth/profile/` — Get/update profile

### Tickets
- `GET /api/tickets/` — List tickets
- `POST /api/tickets/` — Create ticket
- `GET /api/tickets/{id}/` — Get ticket details
- `PATCH /api/tickets/{id}/status/` — Update status
- `POST /api/tickets/{id}/escalate/` — Escalate to HQ

### Missions
- `GET /api/missions/` — List all 70 missions
- `GET /api/missions/{id}/` — Mission details
- `GET /api/missions/categories/` — Ticket categories

### Dashboard
- `GET /api/dashboard/overview/` — Dashboard stats
- `GET /api/dashboard/trends/` — Ticket trends
- `GET /api/dashboard/missions/` — Mission statistics

---

## Development Workflow

### Making Changes

1. **Backend changes:**
   - Edit files in `apps/`
   - If models changed: `python manage_supabase.py makemigrations`
   - Apply: `python manage_supabase.py migrate`
   - Restart server

2. **Frontend changes:**
   - Edit files in `frontend/src/`
   - Hot reload is automatic
   - No restart needed

### Creating New Users

**Via Django Admin:**
1. Go to http://localhost:8000/admin/
2. Login with superuser credentials
3. Navigate to Users → Add User

**Via Frontend:**
1. Login as HQ Super Admin
2. Navigate to Users → Add User
3. Fill in details and assign mission

---

## Next Steps

1. ✅ **Explore the system** — Create tickets, assign agents, test workflows
2. ✅ **Create test users** — Add users for different missions and roles
3. ✅ **Test mission isolation** — Verify users only see their mission's data
4. ✅ **Test escalation** — Escalate a ticket to HQ
5. ✅ **Review dashboard** — Check analytics and reports

---

## Support & Documentation

- **Full Documentation:** See `README.md`
- **Requirements Spec:** See `pdf1_content.txt` and `pdf2_content.txt`
- **Setup Guide:** See `SETUP.md`
- **Supabase Setup:** See `SUPABASE_SETUP.md`

---

## Production Deployment

**⚠️ Before deploying to production:**

1. Change `DEBUG=False` in settings
2. Set strong `SECRET_KEY`
3. Configure proper `ALLOWED_HOSTS`
4. Use production-grade database (not Supabase free tier)
5. Set up SSL/TLS (HTTPS)
6. Configure email backend (SendGrid)
7. Enable virus scanning for file uploads
8. Set up monitoring and logging
9. Configure backups
10. Review security checklist

---

**🎉 You're all set! Happy coding!**

Ministry of Foreign and Diaspora Affairs, Kenya  
Helpdesk Ticket Management System (HTMS)
