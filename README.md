🚀 MockMate AI
AI-Powered Interview Preparation & Resume Intelligence Platform

MockMate AI is a production-ready, AI-driven career preparation platform built with Django and Groq AI (Llama 3.3 70B).
It helps students and job seekers optimize resumes, practice interviews, and track performance through intelligent analytics and feedback systems.

✨ Key Features
🤖 AI Mock Interviews
AI-generated technical and HR interview questions
Personalized, context-aware feedback
Real-time evaluation of responses
Interview performance tracking over time
📄 AI Resume Analyzer
Upload and analyze PDF resumes
ATS compatibility scoring (0–100)
Identification of strengths and weaknesses
Keyword optimization suggestions
Resume structure and formatting evaluation
📊 Analytics Dashboard
Track interview performance history
Identify weak technical and behavioral areas
Personalized improvement roadmap
Smart practice recommendations powered by AI insights
🔐 Authentication System
Secure user registration and login
Profile management
Persistent storage of resumes and interview history
🛠️ Tech Stack
Backend
Python
Django 4.2
AI Integration
Groq API
Llama 3.3 70B Versatile
Prompt Engineering
Frontend
HTML5
CSS3
Bootstrap 5
JavaScript
Database
SQLite (Development)
PostgreSQL (Production Ready)
Additional Tools
Django REST Framework
pdfplumber (PDF parsing)
Git & GitHub
📂 Project Architecture
MockMate/
│
├── ai_engine/        # AI logic, prompts & inference layer
├── analytics/        # Performance tracking & insights
├── interviews/       # Mock interview system
├── resumes/          # Resume parsing & ATS analysis
├── users/            # Authentication & profiles
├── templates/        # Frontend HTML templates
├── static/           # CSS, JS, assets
├── media/            # Uploaded resumes & files
├── manage.py
├── requirements.txt
└── README.md
🚀 Setup Instructions
1️⃣ Clone Repository
git clone https://github.com/Rajshekhar061/Mockmate.git
cd Mockmate
2️⃣ Create Virtual Environment
python -m venv venv

Activate:

Windows: venv\Scripts\activate
Linux/Mac: source venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Environment Variables

Create a .env file:

GROQ_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key
DEBUG=True
5️⃣ Run Migrations
python manage.py migrate
6️⃣ Start Server
python manage.py runserver

Open:

https://mockmate-v7if.onrender.com/
🧠 AI Workflow
Resume Upload
      ↓
PDF Text Extraction (pdfplumber)
      ↓
Groq LLM Processing
      ↓
ATS Scoring + Feedback Generation
      ↓
Analytics + Personalized Recommendations
📊 Sample AI Output
{
  "ats_score": 85,
  "strengths": [
    "Strong technical skills section",
    "Well-structured resume format"
  ],
  "weaknesses": [
    "Lacks quantifiable achievements"
  ],
  "suggestions": [
    "Add measurable impact using metrics"
  ]
}
🔒 Security Highlights
Environment variable-based configuration
CSRF protection enabled
Secure authentication system
File upload validation
Structured error handling and logging
🚀 Future Enhancements
🎤 Voice-based AI interviews
📹 Webcam-based confidence analysis
💻 Coding interview simulation
⚛️ React frontend migration
🐳 Docker containerization
☁️ AWS/GCP deployment
📧 Email notifications system
📈 Advanced ML-driven analytics
💡 Skills Demonstrated
Django backend development
AI integration with LLMs
Prompt engineering
REST API design
Authentication & security systems
PDF parsing & file handling
Analytics system design
Database modeling
Full-stack project architecture
Git & deployment workflows

Screenshots-
https://github.com/Rajshekhar061/Mockmate/blob/main/screenshots/homepage.png

📈 Learning Outcomes
Built a full-stack AI-powered SaaS-style application
Learned real-world LLM integration patterns
Designed scalable Django project architecture
Implemented resume parsing + ATS logic
Developed analytics-driven feedback systems
👨‍💻 Author

Rajshekhar Singh

GitHub: Rajshekhar061

⭐ Support

If you like this project:

⭐ Star the repository
🍴 Fork it
💬 Share feedback
📜 License

This project is licensed under the MIT License.

🌟 Vision

MockMate AI aims to become a complete AI-powered career acceleration platform, helping candidates prepare smarter, improve continuously, and perform confidently in real interviews.
