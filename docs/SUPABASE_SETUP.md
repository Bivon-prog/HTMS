# Supabase Setup Guide for HTMS

## Step 1: Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Sign up/login to your account
3. Click "New Project"
4. Select your organization
5. Enter project details:
   - **Project Name**: HTMS-Development
   - **Database Password**: Choose a strong password
   - **Region**: Choose nearest region to you
6. Click "Create new project"
7. Wait for the project to be created (2-3 minutes)

## Step 2: Get Database Credentials

1. Go to your Supabase project dashboard
2. Click on **Settings** → **Database**
3. Scroll down to **Connection string**
4. Copy the **URI** or use individual parameters:
   - **Host**: Your project's hostname (e.g., `abcdefg.supabase.co`)
   - **Database Name**: `postgres`
   - **Port**: `5432`
   - **User**: `postgres`
   - **Password**: Your database password

## Step 3: Update .env.supabase

Edit the `.env.supabase` file with your credentials:

```bash
# Supabase Database Configuration
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=your_actual_password_here
SUPABASE_DB_HOST=your_project_ref.supabase.co
SUPABASE_DB_PORT=5432
```

## Step 4: Run the Application

Once you've updated the credentials:

```bash
# Run setup script
python setup_supabase.py

# Or run manually:
python manage_supabase.py makemigrations
python manage_supabase.py migrate
python manage_supabase.py createsuperuser
python manage_supabase.py runserver
```

## Step 5: Start Frontend

In another terminal:

```bash
cd frontend
npm install
npm start
```

## Access Points

- **Backend API**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8000/admin/
- **Frontend**: http://localhost:3000
- **API Health Check**: http://localhost:8000/api/health/

## Troubleshooting

### Connection Issues
- Ensure your Supabase project is active (not paused)
- Check that the database password is correct
- Verify the hostname matches your Supabase project

### Migration Issues
- Make sure you have the correct database permissions
- Check that the database is accessible from your location

### Frontend Issues
- Ensure the backend is running on port 8000
- Check that CORS is configured correctly

## Default Test Data

After setup, you can access:
- **Admin Panel**: http://localhost:8000/admin/
- **Login**: Use your superuser credentials
- **Create sample missions, users, and tickets**
