# 🚀 CAREERAI - QUICK REFERENCE GUIDE

## ⚡ Quick Commands

### Environment & Setup
```bash
# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (Linux/Mac)
source venv/bin/activate

# Deactivate
deactivate

# Install dependencies
pip install -r requirements.txt

# Update requirements.txt
pip freeze > requirements.txt
```

### Django Management
```bash
# Run development server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Django shell
python manage.py shell

# Run tests
python manage.py test

# Collect static files
python manage.py collectstatic

# Check deployment readiness
python manage.py check --deploy

# Clear database (WARNING!)
python manage.py flush
```

### Database
```bash
# Database shell (SQLite)
python manage.py dbshell

# Database shell (PostgreSQL)
psql -U postgres -d career_ai

# Backup PostgreSQL
pg_dump -U postgres career_ai > backup.sql

# Restore PostgreSQL
psql -U postgres career_ai < backup.sql
```

---

## 📁 Project Structure Quick Reference

```
MockMate/
├── career_ai/          # Main project configuration
├── users/              # User authentication app
├── resumes/            # Resume analysis app
├── ai_engine/          # AI services (Groq integration)
├── templates/          # HTML templates
├── static/             # CSS, JS, images
├── media/              # User uploaded files
├── logs/               # Application logs
└── manage.py           # Django management
```

---

## 🔗 Important URLs

### Development
- **Home**: http://localhost:8000
- **Admin**: http://localhost:8000/admin
- **Register**: http://localhost:8000/auth/register
- **Login**: http://localhost:8000/auth/login
- **Dashboard**: http://localhost:8000/auth/dashboard
- **Upload Resume**: http://localhost:8000/resume/upload

---

## 📝 File Locations

| File | Location | Purpose |
|------|----------|---------|
| Settings | `career_ai/settings.py` | Django configuration |
| URLs | `career_ai/urls.py` | Main URL routing |
| Models | `resumes/models.py` | Database models |
| Views | `resumes/views.py` | Request handlers |
| Forms | `resumes/forms.py` | Form validation |
| Templates | `templates/` | HTML files |
| Static | `static/` | CSS, JS, images |
| Logs | `logs/` | Application logs |
| Environment | `.env` | Configuration |
| Dependencies | `requirements.txt` | Python packages |

---

## 🔐 Security Checklist

- [ ] Never commit `.env` file
- [ ] Change `SECRET_KEY` in production
- [ ] Set `DEBUG=False` in production
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use HTTPS in production
- [ ] Regular security updates
- [ ] Monitor logs for errors
- [ ] Validate all user inputs
- [ ] Use environment variables for secrets

---

## 🐛 Troubleshooting Quick Fixes

### Module Not Found
```bash
pip install -r requirements.txt
```

### Database Errors
```bash
python manage.py migrate
python manage.py makemigrations
python manage.py migrate
```

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Clear Database Cache
```bash
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()
```

---

## 🧪 Testing Quick Reference

```bash
# Run all tests
python manage.py test

# Run specific app
python manage.py test resumes

# Run with coverage
coverage run --source='.' manage.py test
coverage report

# Run specific test
python manage.py test resumes.tests.ResumeUploadTest
```

---

## 🔧 Common Development Tasks

### Adding a New URL Route
1. Create view in `app/views.py`
2. Add to `app/urls.py`
3. Include in `career_ai/urls.py`

### Creating a Migration
```bash
python manage.py makemigrations app_name
python manage.py migrate
```

### Adding a Template
1. Create file in `templates/app/`
2. Use in view: `render(request, 'app/template.html')`
3. Extend base: `{% extends "base.html" %}`

### Adding a Form
1. Create in `app/forms.py`
2. Use in view: `form = MyForm()`
3. Use in template: `{{ form }}`

---

## 📊 Groq API Integration

### Health Check
```python
from ai_engine.services.groq_service import GroqService

groq = GroqService()
is_healthy = groq.health_check()
print(is_healthy)  # True/False
```

### Analyze Resume
```python
from ai_engine.services.groq_service import GroqService

groq = GroqService()
resume_text = "Your resume text here..."
result = groq.analyze_resume(resume_text)
print(result['ats_score'])  # 0-100
```

### Generate Interview Questions
```python
from ai_engine.services.groq_service import GroqService

groq = GroqService()
questions = groq.generate_interview_questions(resume_text, role="Software Engineer")
print(questions['questions'])
```

---

## 🗄️ Database Models

### Resume Model
```python
Resume.objects.create(
    user=request.user,
    uploaded_file=file,
    original_filename="resume.pdf",
    status="processing"
)

# Query
Resume.objects.filter(user=request.user).order_by('-created_at')
Resume.objects.get(id=1)

# Update
resume.ats_score = 85
resume.status = "completed"
resume.save()

# Delete
resume.delete()
```

---

## 🔍 Logging

### View Logs
```bash
# Django logs
tail -f logs/career_ai.log

# Error logs
tail -f logs/errors.log

# Real-time monitoring
tail -F logs/career_ai.log | grep ERROR
```

### Add Logging
```python
import logging

logger = logging.getLogger(__name__)

logger.info("Info message")
logger.error("Error message")
logger.warning("Warning message")
```

---

## 📱 Responsive Design Breakpoints

Bootstrap 5 uses these breakpoints:
- `sm`: 576px (small phones)
- `md`: 768px (tablets)
- `lg`: 992px (laptops)
- `xl`: 1200px (desktops)
- `xxl`: 1400px (large screens)

### Example
```html
<div class="col-md-6 col-lg-4">Content</div>
```

---

## 🎨 CSS Classes Reference

### Bootstrap Buttons
```html
<button class="btn btn-primary">Primary</button>
<button class="btn btn-secondary">Secondary</button>
<button class="btn btn-success">Success</button>
<button class="btn btn-danger">Danger</button>
<button class="btn btn-warning">Warning</button>
<button class="btn btn-info">Info</button>
```

### Bootstrap Alerts
```html
<div class="alert alert-success">Success!</div>
<div class="alert alert-danger">Error!</div>
<div class="alert alert-warning">Warning!</div>
<div class="alert alert-info">Info</div>
```

### Bootstrap Cards
```html
<div class="card">
    <div class="card-header">Title</div>
    <div class="card-body">Content</div>
    <div class="card-footer">Footer</div>
</div>
```

---

## 🛠️ Useful Django Query Examples

```python
# Filtering
Resume.objects.filter(ats_score__gte=80)
Resume.objects.filter(status='completed')
Resume.objects.filter(user=request.user)

# Ordering
Resume.objects.order_by('-created_at')
Resume.objects.order_by('ats_score')

# Aggregation
from django.db.models import Avg, Count
Resume.objects.aggregate(avg_score=Avg('ats_score'))
Resume.objects.count()

# Relationships
user_resumes = User.objects.get(id=1).resumes.all()

# Excluding
Resume.objects.exclude(status='failed')

# Limiting
Resume.objects.all()[:10]

# Existence
Resume.objects.filter(id=1).exists()
```

---

## 📤 Deployment Commands

### Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Run with Gunicorn
```bash
pip install gunicorn
gunicorn career_ai.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### Docker Build
```bash
docker build -t career-ai .
docker run -p 8000:8000 -e GROQ_API_KEY=your_key career-ai
```

---

## 💻 Code Style

### Import Order
```python
# Standard library
import os
import sys

# Third-party
from django.shortcuts import render
from groq import Groq

# Local
from .models import Resume
from .utils import extract_text
```

### Function Documentation
```python
def extract_text_from_pdf(pdf_path: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Extract text from PDF file.
    
    Args:
        pdf_path (str): Path to PDF file
        
    Returns:
        Tuple[bool, Optional[str], Optional[str]]: (success, text, error)
    """
    pass
```

---

## 🚨 Error Handling Pattern

```python
try:
    # Your code
    result = some_operation()
except ValueError as e:
    logger.error(f"Value error: {str(e)}")
    messages.error(request, "Invalid input")
    return redirect('home')
except Exception as e:
    logger.error(f"Unexpected error: {str(e)}", exc_info=True)
    messages.error(request, "An error occurred")
    return redirect('home')
```

---

## 🎯 Quick Tips

1. **Always use virtual environments**
2. **Never commit sensitive data to git**
3. **Use type hints for better code**
4. **Write meaningful commit messages**
5. **Test before deploying**
6. **Check logs for errors**
7. **Use migrations for database changes**
8. **Keep static files organized**
9. **Use environment variables**
10. **Document your code**

---

## 📞 When You Need Help

1. Check **README.md** - General overview
2. Check **SETUP_GUIDE.md** - Setup issues
3. Check **IMPLEMENTATION_SUMMARY.md** - Implementation details
4. Check **logs/** - Application errors
5. Set `DEBUG=True` - See detailed error messages
6. Check Django documentation
7. Check Groq API documentation

---

**Last Updated**: May 4, 2026
**Version**: 1.0.0
