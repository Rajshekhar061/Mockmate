# CareerAI - AI-Powered Interview Preparation Platform

> Production-quality AI-powered interview preparation platform for students built with Django, Groq AI, and PostgreSQL.

## 🎯 Features

### Resume Analysis MVP
- **AI-Powered Resume Analysis**: Upload PDF resumes and get instant ATS scores (0-100)
- **Detailed Feedback**: Get strengths, weaknesses, and actionable suggestions
- **Keyword Optimization**: Identify missing keywords and optimize for ATS
- **Formatting Analysis**: Check resume formatting quality and consistency

### User Management
- **Secure Authentication**: User registration, login, and profile management
- **Dashboard**: Track all uploaded resumes and analysis history
- **Secure File Storage**: Encrypted storage for user resumes

### Tech Stack
- **Backend**: Django 4.2.10
- **Database**: PostgreSQL (with SQLite for development)
- **AI Engine**: Groq API (llama-3.3-70b-versatile model)
- **Frontend**: Bootstrap 5, Responsive Design
- **PDF Processing**: pdfplumber for text extraction
- **REST API**: Django REST Framework

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL (optional, SQLite works for development)
- Groq API Key (get from https://console.groq.com)

### Installation

1. **Clone the repository**
```bash
cd c:\Users\shekh\OneDrive\Desktop\MockMate
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
# Copy .env.example to .env
cp .env .env

# Edit .env and add your Groq API key:
# GROQ_API_KEY=your_api_key_here
# DEBUG=True
# SECRET_KEY=your-secret-key
```

5. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser (admin)**
```bash
python manage.py createsuperuser
# Follow prompts to create admin account
```

7. **Run development server**
```bash
python manage.py runserver
```

8. **Access the application**
- Home: http://localhost:8000
- Admin: http://localhost:8000/admin

## 📁 Project Structure

```
MockMate/
├── career_ai/                  # Main project config
│   ├── settings.py            # Django settings
│   ├── urls.py                # Main URL configuration
│   ├── wsgi.py                # WSGI config
│   └── error_handler.py       # Error handling utilities
├── users/                     # User authentication app
│   ├── models.py
│   ├── views.py               # Auth views (register, login, logout, dashboard)
│   ├── forms.py               # Auth forms
│   ├── urls.py
│   └── admin.py
├── resumes/                   # Resume analysis app
│   ├── models.py              # Resume model
│   ├── views.py               # Resume upload and analysis views
│   ├── forms.py               # Resume upload form
│   ├── urls.py
│   ├── admin.py
│   └── utils/
│       └── pdf_extractor.py   # PDF text extraction
├── ai_engine/                 # AI service app
│   ├── services/
│   │   └── groq_service.py    # Groq API integration
│   └── prompts/
│       └── resume_prompt.py   # AI prompts for analysis
├── interviews/                # Mock interviews (future feature)
├── analytics/                 # Analytics tracking (future feature)
├── templates/                 # HTML templates
│   ├── base.html              # Base template with navbar/footer
│   ├── home.html              # Home page
│   ├── users/
│   │   ├── register.html
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   └── profile.html
│   └── resumes/
│       ├── upload_resume.html
│       ├── resume_feedback.html
│       └── resume_list.html
├── static/                    # Static files (CSS, JS, images)
├── media/                     # User uploads (resumes)
├── logs/                      # Application logs
├── .env                       # Environment variables
├── requirements.txt           # Python dependencies
├── manage.py
└── README.md
```

## 🔧 Core Components

### 1. Resume Model (`resumes/models.py`)
```python
- user: ForeignKey to User
- uploaded_file: PDF file upload
- extracted_text: Extracted text from PDF
- ats_score: Integer (0-100)
- strengths, weaknesses, suggestions: JSON fields
- status: uploaded, processing, completed, failed
```

### 2. PDF Extraction (`resumes/utils/pdf_extractor.py`)
- `extract_text_from_pdf()`: Extracts text from PDF files
- `get_pdf_metadata()`: Get PDF information
- `is_searchable_pdf()`: Verify PDF contains text

### 3. Groq AI Service (`ai_engine/services/groq_service.py`)
```python
GroqService class with methods:
- analyze_resume(resume_text, job_description): Analyze resume
- generate_interview_questions(resume_text, role): Generate questions
- generate_response(prompt, system_message): Generic AI response
- health_check(): Test API connection
```

### 4. Views and URL Routing

**Users App** (`users/urls.py`):
- `/auth/register/` - User registration
- `/auth/login/` - User login
- `/auth/logout/` - User logout
- `/auth/dashboard/` - User dashboard
- `/auth/profile/` - User profile

**Resumes App** (`resumes/urls.py`):
- `/resume/upload/` - Upload resume
- `/resume/feedback/<id>/` - View analysis results
- `/resume/list/` - List all resumes
- `/resume/delete/<id>/` - Delete resume
- `/resume/reanalyze/<id>/` - Reanalyze resume

## 📊 API Response Format

### Resume Analysis Response
```json
{
  "ats_score": 78,
  "strengths": [
    {
      "title": "Strong Technical Skills",
      "description": "Well-organized skills section with relevant technologies",
      "impact": "high"
    }
  ],
  "weaknesses": [
    {
      "title": "Vague Job Descriptions",
      "description": "Job descriptions lack quantifiable achievements",
      "severity": "medium"
    }
  ],
  "suggestions": [
    {
      "title": "Add Quantifiable Metrics",
      "action": "Replace vague descriptions with metrics and results",
      "priority": "high",
      "expected_impact": "15-20% boost"
    }
  ],
  "keywords_analysis": {
    "keywords_found": ["Python", "Django", "REST API"],
    "missing_keywords": ["AWS", "Docker", "CI/CD"],
    "keyword_frequency": {"Python": 5, "Django": 3}
  },
  "formatting_quality": {
    "score": 82,
    "issues": ["Inconsistent bullet points"],
    "recommendations": ["Use consistent formatting"]
  }
}
```

## 🔑 Environment Variables

Create `.env` file:
```bash
# Django
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite by default for development)
USE_POSTGRES=False
# For PostgreSQL:
# USE_POSTGRES=True
# DB_NAME=career_ai
# DB_USER=postgres
# DB_PASSWORD=your_password
# DB_HOST=localhost
# DB_PORT=5432

# Groq API
GROQ_API_KEY=your_groq_api_key_here
```

## 📝 Database Migrations

```bash
# Create migrations
python manage.py makemigrations

# List pending migrations
python manage.py showmigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run specific app migration
python manage.py migrate resumes
```

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test resumes

# Run with verbosity
python manage.py test --verbosity=2

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 🔐 Security Checklist

- [ ] Change `SECRET_KEY` in production
- [ ] Set `DEBUG=False` in production
- [ ] Configure `ALLOWED_HOSTS` properly
- [ ] Use HTTPS in production
- [ ] Set up CSRF protection
- [ ] Implement rate limiting
- [ ] Validate all file uploads
- [ ] Use environment variables for secrets
- [ ] Enable SQL injection protection
- [ ] Set up proper logging

## 🚀 Deployment

### Using Gunicorn and Nginx

```bash
# Install production dependencies
pip install gunicorn whitenoise

# Create production requirements
pip freeze > requirements-prod.txt

# Run with Gunicorn
gunicorn career_ai.wsgi:application --bind 0.0.0.0:8000
```

### Using Docker

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "career_ai.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## 📊 Analytics and Monitoring

Application logs are stored in `logs/` directory:
- `logs/career_ai.log` - General application logs
- `logs/errors.log` - Error logs

Configure log levels in `settings.py` for different environments.

## 🤖 AI Model Information

**Model**: Groq Llama 3.3 70B Versatile
- Fast inference with Groq GroqCloud
- Optimized for reasoning and analysis
- Handles complex resume analysis tasks
- Cost-effective for MVP phase

## 🔄 Workflow

1. **User Registration & Login**
   - Create account or login
   - Dashboard shows resume history

2. **Resume Upload**
   - Upload PDF file (max 5MB)
   - System validates file type
   - PDF text extraction starts

3. **AI Analysis**
   - Groq AI analyzes resume content
   - Generates ATS score (0-100)
   - Identifies strengths and weaknesses
   - Provides actionable suggestions

4. **Results Display**
   - Show ATS score with visual indicator
   - Display analysis in organized format
   - Allow users to reanalyze improved resumes
   - Track improvements over time

## 📈 Future Features

- [ ] Mock interview practice with voice recording
- [ ] Interview question generation specific to job roles
- [ ] Career path recommendations
- [ ] Job matching based on resume analysis
- [ ] Premium features with Stripe integration
- [ ] Email notifications
- [ ] Batch resume uploads
- [ ] Resume templates
- [ ] LinkedIn profile import
- [ ] Video interview practice

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 💬 Support

For issues, questions, or suggestions:
- Create an issue on GitHub
- Contact: support@careerai.com

## 🎓 Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Groq API Documentation](https://console.groq.com/docs)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## ✨ Acknowledgments

- Groq for their powerful AI API
- Django community for the excellent framework
- Bootstrap team for responsive CSS framework
- All contributors and users

---

**Built with ❤️ for students preparing for their dream jobs**

Last Updated: May 4, 2026
Version: 1.0.0 MVP
