# HTMS - Helpdesk Ticket Management System

A comprehensive helpdesk ticket management system for the Ministry of Foreign and Diaspora Affairs of Kenya, built with Django REST Framework and React.

## 🚀 Features

### Core Functionality
- **User Management**: Role-based access control (Requester, Agent, Mission Admin, HQ Super Admin)
- **Ticket Management**: Create, assign, track, and resolve tickets
- **Mission Isolation**: Separate data access per diplomatic mission
- **Audit Trail**: Complete tracking of all ticket actions
- **Notifications**: In-app and email notifications
- **Dashboard**: Comprehensive reporting and analytics

### Advanced Features
- **SLA Management**: Complex SLA calendars and localized working hours
- **Asset Management**: Link tickets to assets and inventory
- **Delegation Workflows**: Out-of-office and delegation support
- **File Handling**: Secure file uploads with attachment sanitization
- **Internationalization**: Multi-language support for submission portal
- **On-Behalf-Of (OBO)**: Staff can submit tickets for others

## 🛠 Technology Stack

### Backend
- **Framework**: Django 4.2+ with Django REST Framework
- **Database**: SQLite (default), PostgreSQL, or Appwrite
- **Authentication**: JWT tokens with refresh mechanism
- **Background Tasks**: Celery with Redis
- **Email**: SendGrid integration

### Frontend
- **Framework**: React 18+
- **UI Library**: Material-UI (MUI)
- **State Management**: React Query
- **Routing**: React Router
- **Charts**: Recharts
- **Internationalization**: i18next

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- Redis (for background tasks)
- PostgreSQL or SQLite (for database)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Bivon-prog/HTMS.git
cd HTMS
```

### 2. Backend Setup

#### Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
# Set SECRET_KEY, database credentials, email settings, etc.
```

#### Database Setup
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic
```

#### Start Backend Server
```bash
python manage.py runserver
```

### 3. Frontend Setup

#### Install Dependencies
```bash
cd frontend
npm install
```

#### Environment Configuration
```bash
# Create environment file
cp .env.example .env.local

# Edit with your API URL
REACT_APP_API_URL=http://localhost:8000/api
```

#### Start Frontend Server
```bash
npm start
```

## 🔧 Configuration

### Database Options

#### SQLite (Default)
```env
DATABASE_URL=sqlite:///htms.db
```

#### PostgreSQL
```env
DB_NAME=htms
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

#### Appwrite
```env
APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
APPWRITE_PROJECT_ID=your_project_id
APPWRITE_API_KEY=your_api_key
APPWRITE_DATABASE_ID=your_database_id
```

### Email Configuration
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

## 📊 Access Points

### Development
- **Backend API**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8000/admin/
- **Frontend**: http://localhost:3000

### Default Credentials
- **Admin Email**: admin@htms.go.ke
- **Password**: admin123 (change in production)

## 🏗 Project Structure

```
HTMS/
├── apps/
│   ├── authentication/    # User management & auth
│   ├── tickets/           # Ticket management
│   ├── missions/          # Mission management
│   ├── dashboard/        # Analytics & reporting
│   ├── notifications/     # Notification system
│   └── assets/           # Asset management
├── frontend/             # React frontend
├── htms/                 # Django project settings
├── docs/                 # Documentation
├── requirements.txt      # Python dependencies
├── manage.py            # Django management script
└── .env.example         # Environment template
```

## 🧪 Testing

### Backend Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.authentication

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🚀 Deployment

### Production Deployment

#### Backend
1. Set `DEBUG=False` in production
2. Configure production database
3. Set up Redis for Celery
4. Configure email service
5. Collect static files
6. Use Gunicorn as WSGI server

#### Frontend
1. Build for production
```bash
npm run build
```
2. Deploy to static hosting service

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d
```

## 🔐 Security Considerations

- Change default admin credentials in production
- Use environment variables for sensitive data
- Enable HTTPS in production
- Regular security updates
- Audit logging enabled by default

## 📝 API Documentation

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/refresh/` - Refresh token

### Tickets
- `GET /api/tickets/` - List tickets
- `POST /api/tickets/` - Create ticket
- `GET /api/tickets/{id}/` - Get ticket details
- `PUT /api/tickets/{id}/` - Update ticket
- `DELETE /api/tickets/{id}/` - Delete ticket

### Users
- `GET /api/users/` - List users
- `GET /api/users/{id}/` - Get user details
- `PUT /api/users/{id}/` - Update user

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is proprietary to the Ministry of Foreign and Diaspora Affairs of Kenya.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Contact the development team

## 🔄 Version History

- **v1.0.0** - Initial release with core functionality
- **v1.1.0** - Added Appwrite integration
- **v1.2.0** - Enhanced security features
- **v1.3.0** - Improved UI/UX and performance

## 📊 System Requirements

### Minimum Requirements
- **RAM**: 4GB
- **Storage**: 10GB
- **CPU**: 2 cores
- **Network**: 1Mbps

### Recommended Requirements
- **RAM**: 8GB
- **Storage**: 50GB
- **CPU**: 4 cores
- **Network**: 10Mbps

## 🔍 Monitoring and Logging

- Application logs stored in `/logs/`
- Error tracking enabled
- Performance monitoring available
- Audit trail for all user actions

## 🌐 Internationalization

Supported languages:
- English (en)
- Swahili (sw)
- French (fr)
- Arabic (ar)

## 📱 Mobile Compatibility

The frontend is responsive and works on:
- Desktop browsers (Chrome, Firefox, Safari, Edge)
- Tablets (iPad, Android tablets)
- Mobile phones (iOS, Android)

## 🔧 Customization

The system is designed to be customizable:
- Theme colors and branding
- Custom fields for tickets
- Workflow automation
- Integration with external systems
- Custom reports and analytics

## 📈 Performance

- Optimized database queries
- Caching implemented
- Lazy loading for large datasets
- API rate limiting
- CDN support for static assets

## 🚨 Error Handling

- Comprehensive error logging
- User-friendly error messages
- Graceful degradation
- Automatic retry mechanisms
- Health check endpoints
