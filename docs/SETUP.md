# HTMS Setup Guide

## Quick Start Guide

This guide will help you set up the Helpdesk Ticket Management System (HTMS) from scratch.

## Prerequisites

### System Requirements
- **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher
- **Node.js**: 16.0 or higher
- **PostgreSQL**: 12.0 or higher
- **Redis**: 6.0 or higher
- **Git**: Latest version

### Software Installation

#### Windows
1. **Python**: Download from [python.org](https://python.org)
2. **Node.js**: Download from [nodejs.org](https://nodejs.org)
3. **PostgreSQL**: Download from [postgresql.org](https://postgresql.org)
4. **Redis**: Download from [redis.io](https://redis.io)
5. **Git**: Download from [git-scm.com](https://git-scm.com)

#### macOS
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python3 node postgresql redis git
```

#### Linux (Ubuntu)
```bash
# Update package list
sudo apt update

# Install dependencies
sudo apt install python3 python3-pip python3-venv nodejs npm postgresql postgresql-contrib redis-server git
```

## Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd htms
```

### 2. Backend Setup

#### 2.1 Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

#### 2.2 Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt
```

#### 2.3 Database Setup

```bash
# Start PostgreSQL service
# Windows: Start PostgreSQL service from Services
# macOS: brew services start postgresql
# Linux: sudo systemctl start postgresql

# Create database
createdb htms_db

# Create database user (optional)
createuser htms_user
psql -c "ALTER USER htms_user PASSWORD 'your_password';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE htms_db TO htms_user;"
```

#### 2.4 Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your configuration
# Use a text editor or command line:
nano .env  # or use any text editor
```

**Required .env configuration:**
```
SECRET_KEY=your-secret-key-here (generate with: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
DEBUG=True (for development)
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=htms_db
DB_USER=htms_user
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432

# JWT
JWT_SECRET_KEY=your-jwt-secret-key-here
```

#### 2.5 Database Migrations

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate
```

#### 2.6 Create Superuser

```bash
# Create admin user
python manage.py createsuperuser
```

#### 2.7 Load Initial Data (Optional)

```bash
# Create initial categories, missions, etc.
python manage.py loaddata fixtures/initial_data.json
```

#### 2.8 Test Backend

```bash
# Run development server
python manage.py runserver

# Test in another terminal:
curl http://localhost:8000/api/health/
```

### 3. Frontend Setup

#### 3.1 Install Dependencies

```bash
cd frontend
npm install
```

#### 3.2 Environment Configuration

```bash
# Create environment file
echo "REACT_APP_API_URL=http://localhost:8000/api" > .env
```

#### 3.3 Start Frontend

```bash
# Start development server
npm start

# This will open http://localhost:3000 in your browser
```

### 4. Redis Setup (Optional - for background tasks)

```bash
# Start Redis service
# Windows: Start Redis service
# macOS: brew services start redis
# Linux: sudo systemctl start redis

# Test Redis
redis-cli ping
# Should return: PONG
```

### 5. Initial System Configuration

#### 5.1 Login to Admin Panel

1. Navigate to http://localhost:8000/admin/
2. Login with your superuser credentials
3. Configure initial data:
   - Create missions
   - Create ticket categories
   - Set up holiday calendars
   - Create initial users

#### 5.2 Create Sample Data

```bash
# Run management command to create sample data
python manage.py create_sample_data
```

## Verification Checklist

### Backend Verification
- [ ] Django server starts without errors
- [ ] Database migrations completed successfully
- [ ] Admin panel accessible at http://localhost:8000/admin/
- [ ] API health check responds: http://localhost:8000/api/health/
- [ ] Can create superuser and login to admin

### Frontend Verification
- [ ] React app starts without errors
- [ ] Login page loads at http://localhost:3000
- [ ] Can login with created user
- [ ] Dashboard loads after login
- [ ] Navigation menu works

### Integration Verification
- [ ] Frontend can communicate with backend API
- [ ] User authentication works
- [ ] Can create and view tickets
- [ ] File uploads work
- [ ] Notifications are received

## Common Issues and Solutions

### Backend Issues

**Issue: "ModuleNotFoundError: No module named 'django'"**
```bash
# Solution: Ensure virtual environment is activated
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

**Issue: "FATAL: database "htms_db" does not exist"**
```bash
# Solution: Create database
createdb htms_db
```

**Issue: "OperationalError: FATAL: password authentication failed for user"**
```bash
# Solution: Check database credentials in .env file
# Ensure PostgreSQL user exists with correct password
```

### Frontend Issues

**Issue: "npm ERR! Cannot read property 'match' of undefined"**
```bash
# Solution: Clear npm cache
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

**Issue: "Network Error" when calling API**
```bash
# Solution: Check REACT_APP_API_URL in frontend .env
# Ensure backend server is running
```

### Database Issues

**Issue: "relation does not exist"**
```bash
# Solution: Run migrations
python manage.py migrate
```

**Issue: "permission denied for relation"**
```bash
# Solution: Grant database permissions
psql -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO htms_user;"
```

## Production Deployment

### Backend Production Setup

```bash
# Install production dependencies
pip install gunicorn whitenoise

# Collect static files
python manage.py collectstatic --noinput

# Set environment variables for production
export DEBUG=False
export ALLOWED_HOSTS=yourdomain.com

# Run with Gunicorn
gunicorn htms.wsgi:application --bind 0.0.0.0:8000
```

### Frontend Production Build

```bash
cd frontend
npm run build

# The build directory contains the production files
# Serve with nginx, Apache, or any web server
```

### Database Production Setup

```bash
# Create production database
createdb htms_prod

# Run migrations with production settings
python manage.py migrate --settings=htms.settings.production

# Create superuser
python manage.py createsuperuser
```

## Next Steps

1. **Configure Email Settings**: Set up SMTP for notifications
2. **Set Up SSL/TLS**: Configure HTTPS for production
3. **Configure Monitoring**: Set up logging and monitoring
4. **Load Initial Data**: Import missions, users, and categories
5. **Test Full Workflow**: Verify all functionality works
6. **Train Users**: Provide training documentation

## Support

For setup assistance:
- Check the [README.md](README.md) for detailed documentation
- Review the API documentation at http://localhost:8000/api/docs/
- Contact support at support@htms.go.ke

## Troubleshooting

If you encounter issues:

1. Check the logs for error messages
2. Verify all services are running (PostgreSQL, Redis, Django)
3. Ensure environment variables are correctly set
4. Check network connectivity between frontend and backend
5. Review the troubleshooting section in the main README

---

**Happy Setup!** 🚀
