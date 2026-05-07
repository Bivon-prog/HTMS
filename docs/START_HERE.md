# 🚀 START HERE — HTMS Setup

Follow these steps in order to get your system running.

---

## ✅ Step 1: Install Python Dependencies

```bash
# Make sure you're in the HTMS directory
# Activate virtual environment

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# Install all packages
pip install -r requirements.txt
```

**Expected output:** All packages install successfully

---

## ✅ Step 2: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
# Set SECRET_KEY, database credentials, email settings, etc.
```

**Database Options:**
- **SQLite (default):** No additional configuration needed
- **PostgreSQL:** Set DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
- **Appwrite:** Set APPWRITE_ENDPOINT, APPWRITE_PROJECT_ID, APPWRITE_API_KEY, APPWRITE_DATABASE_ID

---

## ✅ Step 3: Run Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser (you'll be prompted)
python manage.py createsuperuser
```

**When prompted, enter your preferred:**
- Admin email
- First name
- Last name  
- Password

**⚠️ Remember these credentials!**

---

## ✅ Step 4: Start Backend Server

```bash
python manage.py runserver
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
2. **Login with your superuser credentials** (from Step 3)
3. **You should see:** Dashboard with statistics

---

## ✅ Step 8: Verify Everything Works

### Check Dashboard
1. Click **Dashboard** in sidebar
2. You should see statistics and charts

### Create a Test Ticket
1. Click **Tickets** → **Create Ticket**
2. Fill in:
   - Title: "Test ticket"
   - Description: "Testing the system"
   - Category: IT
   - Priority: Medium
3. Click **Submit Ticket**
4. You should see success message
5. Go to **Tickets** → You should see your ticket

### Check User Management
1. Click **Users** in sidebar
2. You should see the user management interface

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

**Test Agent:**
- Email: `agent@test.ke`
- First Name: Test
- Last Name: Agent
- Role: Agent
- Department: IT

### 2. Test Workflows

1. **Logout** (top right menu)
2. **Login as Requester** → Create a ticket
3. **Logout**
4. **Login as Agent** → View ticket, assign to yourself, add comment
5. **Logout**
6. **Login as Admin** → View dashboard stats

---

## Troubleshooting

### Backend won't start
**Error:** `ModuleNotFoundError: No module named 'django'`

**Fix:**
```bash
# Windows
venv\Scripts\activate
pip install -r requirements.txt

# Mac/Linux
source venv/bin/activate
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
1. Check `.env` file configuration
2. Verify database server is running
3. Check connection credentials

### Login fails
**Error:** `Invalid credentials`

**Fix:**
1. Make sure you're using the credentials you created during setup
2. Try resetting: `python manage.py createsuperuser`

---

## Quick Reference

### Backend Commands
```bash
# Start server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Django shell
python manage.py shell
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
- **README.md:** Full documentation
- **.env.example:** Environment configuration template

---

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review README.md for detailed instructions
3. Review Django/React error messages carefully

---

**🎯 Your Goal:** Get to the dashboard and create your first ticket

**🌐 Frontend:** http://localhost:3000  
**🔧 Backend:** http://localhost:8000  
**⚙️ Admin Panel:** http://localhost:8000/admin/

---

**Good luck! 🚀**

*HTMS — Ministry of Foreign and Diaspora Affairs, Kenya*
