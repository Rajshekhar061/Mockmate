MockMate AI 🚀
AI-Powered Interview Preparation & Resume Analysis Platform

MockMate AI is a production-quality AI-powered career preparation platform built using Django and Groq AI.
It helps students and job seekers improve resumes, practice interviews, and track performance using intelligent analytics.

✨ Features
🤖 AI Mock Interviews
AI-generated technical & HR interview questions
Personalized interview feedback
Interview performance tracking
Real-time evaluation system
📄 AI Resume Analyzer
Upload PDF resumes
ATS score generation (0–100)
Resume strengths & weaknesses detection
Keyword optimization suggestions
Formatting quality analysis
📊 Analytics Dashboard
Track interview performance
Identify weak topics
Personalized improvement roadmap
Practice recommendations
🔐 Authentication System
User registration & login
Secure profile management
Resume & interview history tracking
🛠️ Tech Stack
Backend
Python
Django 4.2
AI Integration
Groq API
Llama 3.3 70B Versatile
Prompt Engineering
Frontend
HTML
CSS
Bootstrap 5
JavaScript
Database
SQLite (Development)
PostgreSQL (Production Ready)
Additional Tools
Django REST Framework
pdfplumber
Git & GitHub
📂 Project Structure
MockMate/
│
├── ai_engine/          # AI services & prompts
├── analytics/          # Performance analytics
├── interviews/         # Mock interview system
├── resumes/            # Resume analysis module
├── users/              # Authentication system
├── templates/          # HTML templates
├── static/             # Static assets
├── media/              # Uploaded files
├── manage.py
├── requirements.txt
└── README.md
🚀 Installation
1️⃣ Clone Repository
git clone https://github.com/Rajshekhar061/Mockmate.git
cd Mockmate
2️⃣ Create Virtual Environment
python -m venv venv
Windows
venv\Scripts\activate
Linux/Mac
source venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Configure Environment Variables

Create .env file:

GROQ_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key
DEBUG=True
5️⃣ Run Migrations
python manage.py migrate
6️⃣ Start Development Server
python manage.py runserver

Visit:

http://127.0.0.1:8000/
📸 Screenshots
Dashboard

Resume Analysis

Mock Interview

Analytics

🧠 AI Workflow
User Uploads Resume
        ↓
PDF Text Extraction
        ↓
Groq AI Analysis
        ↓
ATS Score + Feedback
        ↓
Analytics & Recommendations
📊 Sample Resume Analysis Output
{
  "ats_score": 85,
  "strengths": [
    "Strong technical skills section",
    "Well-structured resume"
  ],
  "weaknesses": [
    "Missing quantifiable achievements"
  ],
  "suggestions": [
    "Add metrics and measurable impact"
  ]
}
🔒 Security Features
Environment variable protection
Secure authentication system
CSRF protection
File upload validation
Error handling & logging
🚀 Future Improvements
🎤 Voice-based AI interviews
📹 Webcam confidence analysis
💻 Coding interview rounds
⚛️ React frontend
🐳 Docker deployment
☁️ AWS/GCP deployment
📧 Email notifications
📈 Advanced analytics
💡 Skills Demonstrated
Django Backend Development
AI API Integration
Prompt Engineering
Authentication Systems
File Upload Handling
PDF Processing
Database Design
Analytics Dashboard
REST APIs
Git & GitHub
📈 Learning Outcomes

This project helped in learning:

Full-stack Django development
AI-powered application workflows
Resume parsing systems
Analytics & recommendation systems
Production-ready project structure
Git & GitHub workflows
🤝 Contributing
Fork the repository
Create a feature branch
Commit your changes
Push to the branch
Open a Pull Request
👨‍💻 Author

Rajshekhar Singh

GitHub:
Rajshekhar061 GitHub Profile

⭐ Support

If you like this project:

Star the repository
Fork the project
Share feedback
📜 License

This project is licensed under the MIT License.

🌟 Project Vision

MockMate AI aims to become a complete AI-powered career preparation platform that helps students prepare smarter, improve faster, and perform confidently in real interviews.
