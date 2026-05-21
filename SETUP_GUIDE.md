# CareerAI - Complete Setup Guide

## System Requirements

- **OS**: Windows, macOS, or Linux
- **Python**: 3.8 or higher
- **RAM**: 2GB minimum (4GB recommended)
- **Disk Space**: 2GB minimum
- **Database**: PostgreSQL 12+ (optional, SQLite for development)

## Step-by-Step Setup

### 1. Initial Setup

```bash
# Navigate to project directory
cd c:\Users\shekh\OneDrive\Desktop\MockMate

# Create Python virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (Linux/Mac)
source venv/bin/activate
```

### 2. Install Dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

### 3. Environment Configuration

```bash
# The .env file should already exist
# Edit it with your settings:

DEBUG=True
SECRET_KEY=django-insecure-your-secret-key-change-in-production
GROQ_API_KEY=your_groq_api_key_here
USE_POSTGRES=False
ALLOWED_HOSTS=localhost,127.0.0.1
```

**To get Groq API Key:**
1. Go to https://console.groq.com
2. Sign up for free account
3. Create API key
4. Add to `.env` file

### 4. Database Setup

#### Option A: SQLite (Development - Default)
```bash
# No additional setup needed
# SQLite database will be created automatically
```

#### Option B: PostgreSQL (Production)

```bash
# Install PostgreSQL
# Then configure .env:
USE_POSTGRES=True
DB_NAME=career_ai
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Run Migrations

```bash
# Create migration files
python manage.py makemigrations

# View pending migrations
python manage.py showmigrations

# Apply migrations to database
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser
# Follow the prompts to create admin user
```

### 6. Create Test Data (Optional)

```bash
# Create a script to add sample data
python manage.py shell
```

### 7. Run Development Server

```bash
# Start Django development server
python manage.py runserver

# Server will run at http://localhost:8000
```

### 8. Access Application

- **Home Page**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin (use superuser credentials)
- **Register**: http://localhost:8000/auth/register/
- **Login**: http://localhost:8000/auth/login/

## Key Commands Reference

### Django Management Commands

```bash
# Run development server
python manage.py runserver

# Run tests
python manage.py test

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Access Django shell
python manage.py shell

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Check deployment readiness
python manage.py check --deploy
```

### Database Commands

```bash
# Database shell (SQLite)
python manage.py dbshell

# Database shell (PostgreSQL)
psql -U postgres -d career_ai

# Reset database (WARNING: deletes all data)
python manage.py flush

# Show SQL for migrations
python manage.py sqlmigrate resumes 0001
```

### Useful Python Commands

```bash
# Activate virtual environment
venv\Scripts\activate

# Deactivate virtual environment
deactivate

# List installed packages
pip list

# Generate requirements.txt
pip freeze > requirements.txt

# Install specific version
pip install Django==4.2.10
```

## Testing Workflow

### 1. Manual Testing

```bash
# Start server
python manage.py runserver

# Test in browser:
# 1. Register new account
# 2. Login with account
# 3. Go to dashboard
# 4. Upload resume
# 5. View analysis results
```

### 2. Automated Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test resumes

# Run specific test class
python manage.py test resumes.tests.ResumeUploadTest

# Run with coverage report
coverage run --source='.' manage.py test
coverage report
coverage html  # Create HTML report
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'groq'"

**Solution:**
```bash
pip install groq
pip install -r requirements.txt
```

### Issue: "psycopg2: connection refused"

**Solution:**
```bash
# Check PostgreSQL is running
# Update DB credentials in .env
# Or use SQLite instead: USE_POSTGRES=False
```

### Issue: "No such table: resumes_resume"

**Solution:**
```bash
# Run migrations
python manage.py migrate
python manage.py makemigrations
python manage.py migrate
```

### Issue: "Static files not loading"

**Solution:**
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check STATIC_URL and STATIC_ROOT in settings.py
```

### Issue: "CSRF token missing or invalid"

**Solution:**
- Ensure cookies are enabled in browser
- Clear browser cache and cookies
- Check CSRF middleware is enabled in settings.py

### Issue: "Groq API errors"

**Solution:**
```bash
# Verify API key in .env
# Check internet connection
# Test API directly:
python manage.py shell
from ai_engine.services.groq_service import GroqService
groq = GroqService()
print(groq.health_check())
```

## Performance Optimization

### 1. Database Optimization

```bash
# Create indexes for frequently queried fields
python manage.py migrate

# In models.py, add indexes:
class Meta:
    indexes = [
        models.Index(fields=['user', '-created_at']),
    ]
```

### 2. Caching

```python
# Add caching to settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
```

### 3. Query Optimization

```python
# Use select_related and prefetch_related
Resume.objects.select_related('user').prefetch_related('suggestions')
```

## Production Deployment

### Checklist

- [ ] Set `DEBUG=False`
- [ ] Change `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up PostgreSQL database
- [ ] Configure static files with WhiteNoise
- [ ] Set up HTTPS/SSL
- [ ] Configure logging
- [ ] Set up backups
- [ ] Configure error monitoring
- [ ] Set up CDN for static files

### Using Gunicorn

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn career_ai.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### Using Docker

```bash
# Build image
docker build -t career-ai .

# Run container
docker run -p 8000:8000 -e GROQ_API_KEY=your_key career-ai
```

## Monitoring and Maintenance

### Check Application Health

```bash
# Run checks
python manage.py check

# Run deployment checks
python manage.py check --deploy
```

### View Logs

```bash
# Django logs
tail -f logs/career_ai.log

# Error logs
tail -f logs/errors.log

# Real-time monitoring
tail -F logs/career_ai.log | grep ERROR
```

### Database Maintenance

```bash
# Backup database
pg_dump -U postgres career_ai > backup.sql

# Restore database
psql -U postgres career_ai < backup.sql

# Check database size
python manage.py shell
from django.db import connection
from django.db.backends.utils import truncate_name
for model in django.apps.apps.get_models():
    print(model._meta.db_table)
```

## Development Best Practices

### Code Style

```bash
# Install linters
pip install black flake8 isort

# Format code
black .

# Check style
flake8 .

# Sort imports
isort .
```

### Git Workflow

```bash
# Initialize git repo
git init

# Add remote
git remote add origin <your-repo-url>

# Create feature branch
git checkout -b feature/your-feature

# Commit changes
git add .
git commit -m "Add your feature"

# Push to remote
git push origin feature/your-feature
```

### Testing Best Practices

```bash
# Write tests
# Create test_models.py, test_views.py, test_forms.py

# Run tests with coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

## Additional Resources

### Documentation Links
- Django: https://docs.djangoproject.com/
- PostgreSQL: https://www.postgresql.org/docs/
- Groq: https://console.groq.com/docs
- Bootstrap: https://getbootstrap.com/docs/5.0/

### Tutorials
- Django for Beginners: https://djangoforbeginners.com/
- Django REST Framework: https://www.django-rest-framework.org/
- PostgreSQL Tutorial: https://www.postgresql.org/docs/current/tutorial.html

### Community
- Django Community: https://www.djangoproject.com/community/
- Stack Overflow: Django tag
- Reddit: r/django

## Support and Help

If you encounter issues:

1. **Check Logs**: Look in `logs/` directory
2. **Read Error Messages**: Usually indicate the problem
3. **Search Documentation**: Django, Groq, PostgreSQL docs
4. **Ask in Community**: Stack Overflow, Reddit r/django
5. **Debug Mode**: Set `DEBUG=True` to see detailed errors

---

**Setup completed successfully!**

Your CareerAI platform is ready for development. 

Next steps:
1. Visit http://localhost:8000
2. Create a user account
3. Upload your first resume
4. Get AI-powered feedback!

Happy learning! 🚀
