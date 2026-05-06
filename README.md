# HTMS — Helpdesk Ticket Management System

**Ministry of Foreign and Diaspora Affairs, Kenya**

A comprehensive helpdesk ticket management system designed to support all 70 Kenyan diplomatic missions worldwide, enabling staff to raise, track, and resolve issues across IT, HR, and facilities departments from a centralized platform.

---

## 🚀 Quick Start

**New to the project? Start here:**

```bash
# 1. Activate virtual environment
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run complete setup
python scripts/setup_complete.py

# 4. Start backend
python manage_supabase.py runserver

# 5. Start frontend (new terminal)
cd frontend && npm install && npm start
```

**📖 Detailed guide:** See [`docs/START_HERE.md`](docs/START_HERE.md)

---

## 📁 Project Structure

```
HTMS/
├── docs/                          # 📚 All documentation
│   ├── START_HERE.md             # ⭐ Begin here
│   ├── QUICKSTART.md             # Step-by-step setup
│   ├── SETUP.md                  # Detailed setup guide
│   ├── FIXES_APPLIED.md          # Changelog
│   ├── READY_TO_RUN.md           # System overview
│   ├── SUPABASE_SETUP.md         # Supabase configuration
│   ├── pdf1_content.txt          # Requirements specification
│   └── pdf2_content.txt          # Design notes
│
├── scripts/                       # 🛠️ Setup & utility scripts
│   ├── setup_complete.py         # One-command setup
│   └── setup_supabase.py         # Supabase-specific setup
│
├── apps/                          # 🐍 Django applications
│   ├── authentication/           # User auth & JWT
│   ├── tickets/                  # Ticket management
│   ├── missions/                 # 70 missions + categories
│   ├── assets/                   # Asset tracking
│   ├── notifications/            # Notification system
│   ├── dashboard/                # Analytics & reports
│   └── users/                    # User management
│
├── frontend/                      # ⚛️ React frontend
│   ├── src/
│   │   ├── pages/               # UI pages
│   │   ├── components/          # Reusable components
│   │   └── services/            # API services
│   └── package.json
│
├── htms/                          # ⚙️ Django project settings
│   ├── settings.py              # Main settings
│   ├── settings_supabase.py     # Supabase config
│   └── urls.py                  # URL routing
│
├── logs/                          # 📝 Application logs
├── media/                         # 📎 User uploads
├── static/                        # 🎨 Static files
├── venv/                          # 🐍 Python virtual environment
│
├── .env                           # 🔐 Local environment variables
├── .env.supabase                 # 🔐 Supabase credentials
├── .gitignore                    # Git ignore rules
├── manage.py                     # Django management (local)
├── manage_supabase.py            # Django management (Supabase)
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## ✨ Features

### Core Functionality
- ✅ **Ticket Management** — Create, assign, track, and resolve tickets
- ✅ **Multi-Role Support** — Requester, Agent, Mission Admin, HQ Super Admin
- ✅ **Mission Isolation** — Each mission sees only their own data
- ✅ **SLA Management** — Automatic SLA calculations with timezone support
- ✅ **Audit Trail** — Complete audit logging for all actions
- ✅ **File Attachments** — Secure file upload with validation
- ✅ **Notifications** — Email and in-app notifications
- ✅ **Reporting** — Comprehensive dashboards and reports

### Advanced Features
- ✅ **Asset Management** — Track government devices and link to tickets
- ✅ **70 Missions Loaded** — All Kenyan diplomatic missions worldwide
- ✅ **Complex SLA Calendars** — Mission-specific working hours and holidays
- ✅ **Escalation Workflows** — Tier 1 (Mission) → Tier 2 (HQ Nairobi)
- ✅ **Internationalization** — Framework for English, French, Arabic, Mandarin
- ✅ **Role-Based Access** — Granular permissions per role
- ✅ **JWT Authentication** — Secure token-based auth with refresh

---

## 🌍 Missions Coverage

**70 Kenyan Diplomatic Missions:**
- 🌍 **Africa:** 29 missions
- 🌏 **Asia & Oceania:** 11 missions
- 🌍 **Europe:** 13 missions
- 🌍 **Middle East:** 10 missions
- 🌎 **Americas:** 6 missions
- 🏛️ **Multilateral:** 3 missions (UN, UNESCO)

---

## 🔧 Tech Stack

### Backend
- **Framework:** Django 4.2 with Django REST Framework
- **Database:** PostgreSQL (Supabase for development)
- **Authentication:** JWT with SimpleJWT
- **Task Queue:** Celery with Redis
- **Email:** SendGrid (console backend for dev)

### Frontend
- **Framework:** React 18 with Material-UI
- **State Management:** React Query
- **Routing:** React Router v6
- **Charts:** Recharts
- **Forms:** React Hook Form
- **Internationalization:** i18next

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **[START_HERE.md](docs/START_HERE.md)** | ⭐ Quick start checklist |
| **[QUICKSTART.md](docs/QUICKSTART.md)** | Detailed setup guide |
| **[SETUP.md](docs/SETUP.md)** | Installation instructions |
| **[FIXES_APPLIED.md](docs/FIXES_APPLIED.md)** | All fixes & improvements |
| **[READY_TO_RUN.md](docs/READY_TO_RUN.md)** | System overview |
| **[SUPABASE_SETUP.md](docs/SUPABASE_SETUP.md)** | Supabase configuration |
| **[pdf1_content.txt](docs/pdf1_content.txt)** | Requirements specification |
| **[pdf2_content.txt](docs/pdf2_content.txt)** | Design discussion notes |

---

## 🎯 User Roles

| Role | Permissions |
|------|-------------|
| **Requester** | Submit tickets, view own tickets, add comments |
| **Agent** | Manage tickets, assign tickets, add internal notes |
| **Mission Admin** | Manage mission users, view all mission tickets, generate reports |
| **HQ Super Admin** | Full system access, manage all missions, global dashboards |

---

## 🔐 Security Features

- ✅ JWT authentication with token refresh
- ✅ Role-based access control (RBAC)
- ✅ Mission data isolation
- ✅ File upload validation and virus scanning
- ✅ SQL injection protection
- ✅ XSS protection
- ✅ CSRF protection
- ✅ Secure password hashing
- ✅ Audit trail for all actions

---

## 📊 API Endpoints

### Authentication
- `POST /api/auth/login/` — User login
- `POST /api/auth/logout/` — User logout
- `POST /api/auth/refresh/` — Refresh JWT token
- `GET /api/auth/verify/` — Verify token
- `POST /api/auth/password-reset/` — Request password reset
- `POST /api/auth/password-reset-confirm/` — Confirm password reset

### Tickets
- `GET /api/tickets/` — List tickets
- `POST /api/tickets/` — Create ticket
- `GET /api/tickets/{id}/` — Get ticket details
- `PATCH /api/tickets/{id}/status/` — Update status
- `POST /api/tickets/{id}/escalate/` — Escalate to HQ
- `GET /api/tickets/{id}/comments/` — Get comments
- `POST /api/tickets/{id}/comments/` — Add comment

### Missions
- `GET /api/missions/` — List all 70 missions
- `GET /api/missions/{id}/` — Mission details
- `GET /api/missions/categories/` — Ticket categories

### Dashboard
- `GET /api/dashboard/overview/` — Dashboard statistics
- `GET /api/dashboard/trends/` — Ticket trends
- `GET /api/dashboard/missions/` — Mission statistics

**Full API documentation:** See [`docs/READY_TO_RUN.md`](docs/READY_TO_RUN.md)

---

## 🧪 Testing

### Run Backend Tests
```bash
python manage_supabase.py test
```

### Run Frontend Tests
```bash
cd frontend
npm test
```

---

## 🚀 Deployment

### Development (Supabase)
```bash
python scripts/setup_complete.py
python manage_supabase.py runserver
```

### Production
See [`docs/READY_TO_RUN.md`](docs/READY_TO_RUN.md) for production deployment checklist.

---

## 🛠️ Management Commands

```bash
# Load all 70 missions
python manage_supabase.py load_missions

# Create superuser
python manage_supabase.py createsuperuser

# Make migrations
python manage_supabase.py makemigrations

# Apply migrations
python manage_supabase.py migrate

# Django shell
python manage_supabase.py shell

# Collect static files
python manage_supabase.py collectstatic
```

---

## 📝 License

This project is proprietary software developed for the Ministry of Foreign and Diaspora Affairs, Kenya.

---

## 👥 Support

For technical support or questions:
- **Documentation:** See [`docs/`](docs/) folder
- **Setup Issues:** See [`docs/QUICKSTART.md`](docs/QUICKSTART.md)
- **Bug Reports:** Contact system administrator

---

## 📅 Version History

- **v1.0.0** (May 2026) — Initial release
  - Core ticket management
  - 70 missions loaded
  - Asset management
  - Dashboard & reporting
  - Multi-role support

---

## 🙏 Acknowledgments

**Prepared by:** Bivon Moriasi Onyoni  
**Position:** ICT Attaché  
**Organization:** Ministry of Foreign and Diaspora Affairs, Kenya

---

**🎉 Ready to get started? See [`docs/START_HERE.md`](docs/START_HERE.md)**

---

*Last Updated: May 6, 2026*  
*HTMS v1.0 — Ministry of Foreign and Diaspora Affairs, Kenya*
