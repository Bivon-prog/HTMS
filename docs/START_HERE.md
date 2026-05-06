# 🚀 START HERE — HTMS Setup

Follow these steps in order to get your system running.

---

## ✅ Step 1: Install Python Dependencies

```bash
# Make sure you're in the HTMS directory
# Activate virtual environment
venv\Scripts\activate

# Install all packages
pip install -r requirements.txt
```

**Expected output:** All packages install successfully

---

## ✅ Step 2: Verify Supabase Connection

Your `.env.supabase` file should have:
```
SUPABASE_DB_HOST=kdcacxkohwhvlzyszlzv.supabase.co
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=sb_publishable_Est2B-RMn3oRPBzfGGLZ3w_fsSJuJ5y
```

**✅ Already configured — no action needed**

---

## ✅ Step 3: Run Complete Setup

```bash
python scripts/setup_complete.py
```

**This will:**
1. Test database connection
2. Create migrations
3. Apply migrations
4. Load 70 missions
5. Load ticket categories
6. Create admin user (you'll be prompted)
7. Collect static files

**When prompted, enter:**
- Admin email: `admin@htms.go.ke` (or your choice)
- First name: `Admin`
- Last name: `User`
- Password: `admin123` (or your choice)

**⚠️ Remember these credentials!**

---

## ✅ Step 4: Start Backend Server

```bash
python manage_supabase.py runserver
```

**Expected output:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

**✅ Leave this terminal running**

---

## ✅ Step 5: Install Frontend Dependencies

**Open a NEW terminal** (keep backend running)

```bash
cd frontend
npm install
```

**Expected output:** All npm packages install successfully

---

## ✅ Step 6: Start Frontend Server

```bash
npm start
```

**Expected output:**
```
Compiled successfully!
You can now view htms-frontend in the browser.
  Local:            http://localhost:3000
```

**✅ Browser should open automatically**

---

## ✅ Step 7: Login & Test

1. **Browser opens to:** http://localhost:3000
2. **Login with:**
   - Email: `admin@htms.go.ke` (or what you entered)
   - Password: `admin123` (or what you entered)
3. **You should see:** Dashboard with statistics

---

## ✅ Step 8: Verify Everything Works

### Check Missions Loaded
1. Click **Missions** in sidebar
2. You should see **70 missions** listed
3. Try filtering by region (Africa, Europe, etc.)

### Check Categories Loaded
1. Click **Tickets** → **Create Ticket**
2. Category dropdown should show:
   - IT
   - HR
   - Facilities
   - Finance
   - Security
   - Other

### Create a Test Ticket
1. Click **Create Ticket**
2. Fill in:
   - Title: "Test ticket"
   - Description: "Testing the system"
   - Category: IT
   - Priority: Medium
3. Click **Submit Ticket**
4. You should see success message
5. Go to **Tickets** → You should see your ticket

### Check Dashboard
1. Click **Dashboard**
2. You should see:
   - Total tickets: 1
   - Charts with data
   - Statistics

---

## 🎉 Success!

If all the above works, your system is fully operational!

---

## What to Do Next

### 1. Create Test Users

Go to **Users** → **Add User** and create:

**Test Requester:**
- Email: `requester@test.ke`
- First Name: Test
- Last Name: Requester
- Role: Requester
- Mission: Kenya Permanent Mission to UN Nairobi

**Test Agent:**
- Email: `agent@test.ke`
- First Name: Test
- Last Name: Agent
- Role: Agent
- Department: IT
- Mission: Kenya Permanent Mission to UN Nairobi

### 2. Test Workflows

1. **Logout** (top right menu)
2. **Login as Requester** → Create a ticket
3. **Logout**
4. **Login as Agent** → View ticket, assign to yourself, add comment
5. **Logout**
6. **Login as Requester** → View comment, reply
7. **Logout**
8. **Login as Agent** → Mark ticket as resolved
9. **Logout**
10. **Login as Admin** → View dashboard stats

### 3. Explore Features

- **Assets:** Add government devices
- **Missions:** Browse all 70 missions
- **Profile:** Update your profile, change password
- **Tickets:** Test escalation, attachments, internal notes

---

## Troubleshooting

### Backend won't start
**Error:** `ModuleNotFoundError: No module named 'django'`

**Fix:**
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend won't start
**Error:** `npm ERR! Cannot find module`

**Fix:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Can't connect to database
**Error:** `OperationalError: could not connect to server`

**Fix:**
1. Check `.env.supabase` file
2. Verify Supabase project is active
3. Check Supabase dashboard → Settings → Database

### Login fails
**Error:** `Invalid credentials`

**Fix:**
1. Make sure you're using the credentials you entered during setup
2. Try resetting: `python manage_supabase.py createsuperuser`

### Missions not showing
**Fix:**
```bash
python manage_supabase.py load_missions
```

---

## Quick Reference

### Backend Commands
```bash
# Start server
python manage_supabase.py runserver

# Create migrations
python manage_supabase.py makemigrations

# Apply migrations
python manage_supabase.py migrate

# Load missions
python manage_supabase.py load_missions

# Create superuser
python manage_supabase.py createsuperuser

# Django shell
python manage_supabase.py shell
```

### Frontend Commands
```bash
# Install dependencies
npm install

# Start dev server
npm start

# Build for production
npm run build
```

---

## Documentation

- **This file:** Quick start checklist
- **QUICKSTART.md:** Detailed setup guide
- **FIXES_APPLIED.md:** All fixes made
- **READY_TO_RUN.md:** System overview
- **README.md:** Full documentation
- **pdf1_content.txt:** Requirements specification
- **pdf2_content.txt:** Design notes

---

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review `QUICKSTART.md` for detailed instructions
3. Check `FIXES_APPLIED.md` for known issues
4. Review Django/React error messages carefully

---

**🎯 Your Goal:** Get to the dashboard with 70 missions loaded

**📧 Admin Login:** `admin@htms.go.ke` / `admin123` (or your custom credentials)

**🌐 Frontend:** http://localhost:3000  
**🔧 Backend:** http://localhost:8000  
**⚙️ Admin Panel:** http://localhost:8000/admin/

---

**Good luck! 🚀**

*HTMS — Ministry of Foreign and Diaspora Affairs, Kenya*
