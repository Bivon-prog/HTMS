# HTMS — Project Structure

This document explains the organization of the HTMS codebase.

---

## 📁 Root Directory

```
HTMS/
├── docs/                    # 📚 All documentation
├── scripts/                 # 🛠️ Setup & utility scripts
├── apps/                    # 🐍 Django applications
├── frontend/                # ⚛️ React frontend
├── htms/                    # ⚙️ Django project settings
├── logs/                    # 📝 Application logs
├── media/                   # 📎 User uploads
├── static/                  # 🎨 Static files (CSS, JS, images)
├── venv/                    # 🐍 Python virtual environment
├── .env                     # 🔐 Local environment variables
├── .env.supabase           # 🔐 Supabase credentials
├── .gitignore              # Git ignore rules
├── manage.py               # Django management (local DB)
├── manage_supabase.py      # Django management (Supabase)
├── requirements.txt        # Python dependencies
└── README.md               # Main project readme
```

---

## 📚 docs/ — Documentation

All project documentation is centralized here.

```
docs/
├── START_HERE.md           # ⭐ Quick start checklist
├── QUICKSTART.md           # Detailed setup guide
├── SETUP.md                # Installation instructions
├── FIXES_APPLIED.md        # Changelog of all fixes
├── READY_TO_RUN.md         # System overview & API docs
├── SUPABASE_SETUP.md       # Supabase configuration
├── PROJECT_STRUCTURE.md    # This file
├── pdf1_content.txt        # Requirements specification
└── pdf2_content.txt        # Design discussion notes
```

**Start here:** `START_HERE.md`

---

## 🛠️ scripts/ — Setup & Utilities

Automated setup and utility scripts.

```
scripts/
├── setup_complete.py       # One-command complete setup
└── setup_supabase.py       # Redirects to setup_complete.py
```

**Usage:**
```bash
python scripts/setup_complete.py
```

---

## 🐍 apps/ — Django Applications

Django apps following the standard Django app structure.

```
apps/
├── authentication/         # User authentication & JWT
│   ├── management/
│   │   └── commands/
│   │       └── create_htms_superuser.py
│   ├── migrations/
│   ├── models.py          # User model
│   ├── serializers.py     # User serializers
│   ├── views.py           # Auth views (login, logout, etc.)
│   └── urls.py            # Auth endpoints
│
├── tickets/               # Ticket management
│   ├── migrations/
│   ├── models.py          # Ticket, Comment, Attachment, AuditLog
│   ├── serializers.py     # Ticket serializers
│   ├── views.py           # Ticket CRUD, escalation
│   └── urls.py            # Ticket endpoints
│
├── missions/              # Missions & categories
│   ├── management/
│   │   └── commands/
│   │       └── load_missions.py  # Loads 70 missions
│   ├── migrations/
│   ├── models.py          # Mission, HolidayCalendar, TicketCategory
│   ├── serializers.py     # Mission serializers
│   ├── views.py           # Mission CRUD
│   └── urls.py            # Mission endpoints
│
├── assets/                # Asset management
│   ├── migrations/
│   ├── models.py          # Asset, AssetTicketHistory
│   ├── serializers.py     # Asset serializers
│   ├── views.py           # Asset CRUD
│   └── urls.py            # Asset endpoints
│
├── notifications/         # Notification system
│   ├── migrations/
│   ├── models.py          # Notification, NotificationPreference
│   ├── serializers.py     # Notification serializers
│   ├── views.py           # Notification views
│   └── urls.py            # Notification endpoints
│
├── dashboard/             # Analytics & reports
│   ├── migrations/
│   ├── views.py           # Dashboard statistics
│   └── urls.py            # Dashboard endpoints
│
├── users/                 # User management
│   ├── migrations/
│   ├── views.py           # User list view
│   └── urls.py            # User endpoints
│
├── __init__.py
└── permissions.py         # Shared permission classes
```

### Key Models

**User** (`authentication/models.py`)
- Email, role, department, mission, timezone
- Roles: Requester, Agent, Mission_Admin, HQ_Super_Admin

**Ticket** (`tickets/models.py`)
- Ticket number, title, description, category, priority, status
- Requester, assigned agent, mission, linked asset
- SLA due date, escalation flag

**Mission** (`missions/models.py`)
- Name, country, city, region, timezone
- Working hours (start/end, week start/end)

**Asset** (`assets/models.py`)
- Inventory tag, device type, make, model, OS
- Assigned user, mission, warranty dates

---

## ⚛️ frontend/ — React Frontend

React application with Material-UI.

```
frontend/
├── public/
│   └── index.html         # HTML template
│
├── src/
│   ├── components/        # Reusable components
│   │   ├── Auth/
│   │   │   └── ProtectedRoute.js
│   │   └── Layout/
│   │       ├── Navbar.js
│   │       └── Sidebar.js
│   │
│   ├── pages/             # Page components
│   │   ├── Auth/
│   │   │   └── Login.js
│   │   ├── Dashboard/
│   │   │   └── Dashboard.js
│   │   ├── Tickets/
│   │   │   ├── TicketList.js
│   │   │   ├── TicketDetail.js
│   │   │   └── CreateTicket.js
│   │   ├── Assets/
│   │   │   ├── AssetList.js
│   │   │   └── AssetDetail.js
│   │   ├── Users/
│   │   │   └── Users.js
│   │   ├── Missions/
│   │   │   └── Missions.js
│   │   └── Profile/
│   │       └── Profile.js
│   │
│   ├── services/          # API service layer
│   │   ├── authService.js
│   │   ├── ticketService.js
│   │   └── dashboardService.js
│   │
│   ├── App.js             # Main app component
│   ├── index.js           # Entry point
│   ├── i18n.js            # Internationalization config
│   └── index.css          # Global styles
│
└── package.json           # npm dependencies
```

### Key Components

**App.js** — Main routing, auth state management  
**Login.js** — Login form with JWT auth  
**Dashboard.js** — Statistics, charts, metrics  
**TicketList.js** — DataGrid with filters  
**TicketDetail.js** — Full ticket view with comments  
**CreateTicket.js** — Ticket creation form  

---

## ⚙️ htms/ — Django Project Settings

Django project configuration.

```
htms/
├── __init__.py
├── settings.py            # Main settings (local DB)
├── settings_supabase.py   # Supabase settings (development)
├── urls.py                # Root URL configuration
├── wsgi.py                # WSGI entry point
└── asgi.py                # ASGI entry point
```

### Settings Files

**settings.py** — Local PostgreSQL database  
**settings_supabase.py** — Supabase PostgreSQL (development)

**Key configurations:**
- Database (PostgreSQL via Supabase)
- JWT authentication
- CORS settings
- File upload limits
- Logging configuration

---

## 📝 logs/ — Application Logs

Django application logs are written here.

```
logs/
├── .gitkeep
└── django.log             # Created at runtime
```

**Configured in:** `htms/settings.py` and `htms/settings_supabase.py`

---

## 📎 media/ — User Uploads

User-uploaded files (ticket attachments).

```
media/
├── .gitkeep
└── ticket_attachments/    # Created at runtime
```

**Max file size:** 10MB  
**Allowed types:** PDF, JPEG, PNG, DOCX  
**Max per ticket:** 5 files

---

## 🎨 static/ — Static Files

Static assets (CSS, JS, images) collected here.

```
static/
├── .gitkeep
└── (collected at runtime)
```

**Collect static files:**
```bash
python manage_supabase.py collectstatic
```

---

## 🐍 venv/ — Virtual Environment

Python virtual environment (not tracked in git).

```
venv/
├── Include/
├── Lib/
├── Scripts/
│   ├── activate          # Activate script (Windows)
│   ├── python.exe        # Python interpreter
│   └── pip.exe           # Package installer
└── pyvenv.cfg
```

**Activate:**
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

---

## 🔐 Environment Files

### .env
Local development environment variables (not tracked in git).

```env
SECRET_KEY=...
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=htms_db
DB_USER=htms_user
DB_PASSWORD=...
```

### .env.supabase
Supabase development credentials (tracked for team development).

```env
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=...
SUPABASE_DB_HOST=your_project.supabase.co
SUPABASE_DB_PORT=5432
```

**⚠️ In production:** Move to secure secrets management.

---

## 📦 Dependencies

### requirements.txt
Python dependencies for the backend.

**Key packages:**
- Django 4.2.7
- djangorestframework 3.14.0
- djangorestframework-simplejwt 5.3.0
- psycopg2-binary 2.9.9
- django-cors-headers 4.3.1
- celery 5.3.4
- redis 5.0.1

### frontend/package.json
npm dependencies for the frontend.

**Key packages:**
- react 18.2.0
- @mui/material 5.11.10
- react-router-dom 6.8.1
- react-query 3.39.3
- axios 1.3.4
- recharts 2.5.0

---

## 🚀 Management Commands

### Django Management

**Main commands:**
```bash
# Using Supabase
python manage_supabase.py <command>

# Using local DB
python manage.py <command>
```

**Common commands:**
- `runserver` — Start development server
- `makemigrations` — Create migrations
- `migrate` — Apply migrations
- `createsuperuser` — Create admin user
- `shell` — Django shell
- `collectstatic` — Collect static files
- `test` — Run tests

### Custom Commands

**Load missions:**
```bash
python manage_supabase.py load_missions
```

**Create HQ Super Admin:**
```bash
python manage_supabase.py create_htms_superuser \
  --email admin@htms.go.ke \
  --first_name Admin \
  --last_name User \
  --password admin123
```

---

## 🔄 Development Workflow

### 1. Backend Changes

```bash
# Edit files in apps/
# If models changed:
python manage_supabase.py makemigrations
python manage_supabase.py migrate

# Restart server
python manage_supabase.py runserver
```

### 2. Frontend Changes

```bash
# Edit files in frontend/src/
# Hot reload is automatic
# No restart needed
```

### 3. Adding New App

```bash
# Create app
python manage_supabase.py startapp myapp apps/myapp

# Add to INSTALLED_APPS in htms/settings.py
# Create models, views, serializers, urls
# Make migrations
python manage_supabase.py makemigrations myapp
python manage_supabase.py migrate
```

---

## 📊 Database Schema

### Core Tables

**users** — User accounts  
**missions** — 70 diplomatic missions  
**ticket_categories** — IT, HR, Facilities, etc.  
**tickets** — Support tickets  
**ticket_comments** — Ticket comments  
**ticket_attachments** — File uploads  
**audit_logs** — Action audit trail  
**assets** — Government devices  
**notifications** — User notifications  
**holiday_calendars** — Mission holidays  

---

## 🔒 Security

### Protected Directories

- `venv/` — Not tracked in git
- `logs/` — Not tracked in git
- `media/` — Not tracked in git
- `__pycache__/` — Not tracked in git

### Sensitive Files

- `.env` — Not tracked in git
- `.env.supabase` — Tracked (dev only, change for prod)
- `db.sqlite3` — Not tracked in git

---

## 📖 Further Reading

- **Setup Guide:** `START_HERE.md`
- **API Documentation:** `READY_TO_RUN.md`
- **Requirements:** `pdf1_content.txt`
- **Design Notes:** `pdf2_content.txt`

---

*Last Updated: May 6, 2026*  
*HTMS v1.0 — Ministry of Foreign and Diaspora Affairs, Kenya*
