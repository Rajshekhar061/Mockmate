import logging

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db.models import Avg
from .forms import UserRegistrationForm, UserLoginForm

logger = logging.getLogger(__name__)

from groq import Groq
from django.conf import settings

from analytics.services import AnalyticsService
from interviews.models import Interview

client = Groq(api_key=settings.GROQ_API_KEY)

def test_ai(request):

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": "Give interview tips"
            }
        ]
    )

    answer = completion.choices[0].message.content

    return HttpResponse(answer)

@require_http_methods(["GET", "POST"])
def register(request):
    """
    User registration view.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                f'Welcome {user.first_name or user.username}! Your account has been created. Please log in.'
            )
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserRegistrationForm()

    context = {
        'form': form,
        'page_title': 'Register',
    }
    return render(request, 'users/register.html', context)


@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    User login view.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                next_page = request.GET.get('next', 'dashboard')
                return redirect(next_page)
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()

    context = {
        'form': form,
        'page_title': 'Login',
    }
    return render(request, 'users/login.html', context)


@login_required(login_url='login')
@require_http_methods(["POST"])
def logout_view(request):
    """
    User logout view.
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required(login_url='login')
def dashboard(request):
    """
    User dashboard view.
    """
    from resumes.models import Resume
    
    resumes = Resume.objects.filter(user=request.user).order_by('-created_at')
    interviews = Interview.objects.filter(user=request.user).order_by('-created_at')
    average_score = interviews.aggregate(avg_score=Avg('overall_score')).get('avg_score') or 0
    recent_interviews = interviews[:3]
    
    progress = 0
    if resumes.exists() or interviews.exists():
        progress = min(100, int(((resumes.count() + interviews.count()) / 20) * 100))

    try:
        analytics_data = AnalyticsService(request.user).refresh_user_analytics()
    except Exception as exc:
        analytics_data = {}
        messages.warning(request, 'Personalized analytics are currently unavailable.')
        logger.warning(f'Failed to load analytics data: {exc}')

    context = {
        'resumes': resumes,
        'resume_count': resumes.count(),
        'interview_count': interviews.count(),
        'average_interview_score': round(average_score),
        'recent_interviews': recent_interviews,
        'progress': progress,
        'weak_topics': analytics_data.get('weak_topics', []),
        'strong_topics': analytics_data.get('strong_topics', []),
        'recommendations': analytics_data.get('recommendations', []),
        'improvement_areas': analytics_data.get('improvement_areas', []),
        'trend_summary': analytics_data.get('trend_summary', ''),
        'page_title': 'Dashboard',
    }
    return render(request, 'users/dashboard.html', context)


@login_required(login_url='login')
def profile(request):
    """
    User profile view.
    """
    context = {
        'user': request.user,
        'page_title': 'Profile',
    }
    return render(request, 'users/profile.html', context)
