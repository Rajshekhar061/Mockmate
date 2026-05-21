import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db.models import Avg

from .models import Interview, InterviewQuestion
from .forms import InterviewStartForm, InterviewAnswerForm
from ai_engine.services.groq_service import GroqService

logger = logging.getLogger(__name__)


def _default_interview_questions(role: str, difficulty: str, interview_type: str):
    """Generate fallback questions when AI service is unavailable."""
    base_questions = [
        {
            'question': f"Describe a key project you built using {role.title()}.",
            'topic': f'{role.title()} fundamentals',
            'difficulty': difficulty,
        },
        {
            'question': f"How do you approach debugging a challenging problem in {role.title()}?",
            'topic': 'Debugging',
            'difficulty': difficulty,
        },
        {
            'question': f"Explain an important concept in {role.title()} that every engineer should know.",
            'topic': 'Core concepts',
            'difficulty': difficulty,
        },
        {
            'question': f"How would you communicate a technical decision to a non-technical stakeholder?",
            'topic': 'Communication',
            'difficulty': difficulty,
        },
        {
            'question': f"What are common interview pitfalls for {role.title()} candidates, and how do you prepare?",
            'topic': 'Interview readiness',
            'difficulty': difficulty,
        },
    ]
    return base_questions


@login_required(login_url='login')
@require_http_methods(['GET', 'POST'])
def start_interview(request):
    """Start a new interview session and generate questions."""
    if request.method == 'POST':
        form = InterviewStartForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.user = request.user
            interview.save()

            questions = []
            try:
                groq = GroqService()
                result = groq.generate_interview_questions(
                    role=interview.role,
                    difficulty=interview.difficulty,
                    interview_type=interview.interview_type,
                    count=5,
                )
                questions = result.get('questions', [])

                if result.get('error') or not questions:
                    raise ValueError(result.get('error', 'No questions returned by AI'))

            except Exception as e:
                logger.warning(f"Interview question generation failed: {str(e)}")
                messages.warning(
                    request,
                    'AI interview generation failed. Using fallback questions so you can continue.'
                )
                questions = _default_interview_questions(
                    interview.role,
                    interview.difficulty,
                    interview.interview_type,
                )

            for index, question_payload in enumerate(questions, start=1):
                InterviewQuestion.objects.create(
                    interview=interview,
                    order=index,
                    question=question_payload.get('question', ''),
                )

            return redirect('interview_question', interview_id=interview.id, question_index=1)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = InterviewStartForm()

    context = {
        'form': form,
        'page_title': 'Start Mock Interview',
    }
    return render(request, 'interviews/start_interview.html', context)


@login_required(login_url='login')
@require_http_methods(['GET', 'POST'])
def interview_question(request, interview_id, question_index):

    interview = get_object_or_404(Interview, id=interview_id, user=request.user)

    # ✅ FIX: use ordered list instead of DB lookup by "order"
    questions = list(interview.questions.order_by('order'))

    total_questions = len(questions)

    current_index = question_index - 1

    # safety check
    if current_index < 0 or current_index >= total_questions:
        interview.calculate_overall_score()
        return redirect('interview_feedback', interview_id=interview.id)

    question = questions[current_index]

    if request.method == 'POST':
        form = InterviewAnswerForm(request.POST)

        if form.is_valid():
            question.user_answer = form.cleaned_data['user_answer']

            try:
                groq = GroqService()
                feedback = groq.evaluate_interview_answer(
                    question.question,
                    question.user_answer,
                    role=interview.role,
                    difficulty=interview.difficulty,
                    interview_type=interview.interview_type,
                )

                question.ai_feedback = feedback.get('feedback_summary', '')
                question.score = feedback.get('score', 0)
                question.ideal_answer = feedback.get('ideal_answer', '')

            except Exception as e:
                logger.error(f"Interview answer evaluation failed: {str(e)}")
                messages.warning(request, "AI evaluation failed, but answer saved.")

            question.save()

            # ✅ FIX NAVIGATION
            next_index = question_index + 1

            if next_index > total_questions:
                interview.calculate_overall_score()
                return redirect('interview_feedback', interview_id=interview.id)

            return redirect(
                'interview_question',
                interview_id=interview.id,
                question_index=next_index
            )

    else:
        form = InterviewAnswerForm(initial={'user_answer': question.user_answer})

    return render(request, 'interviews/interview_question.html', {
        'interview': interview,
        'question': question,
        'form': form,
        'progress': {
            'current': question_index,
            'total': total_questions,
        },
    })


@login_required(login_url='login')
@require_http_methods(['GET'])
def interview_feedback(request, interview_id):
    """Display AI feedback for a completed interview session."""
    interview = get_object_or_404(Interview, id=interview_id, user=request.user)
    questions = interview.questions.order_by('order')

    if not questions.exists():
        messages.error(request, 'This interview does not contain any questions.')
        return redirect('interview_history')

    context = {
        'interview': interview,
        'questions': questions,
        'page_title': 'Interview Feedback',
    }
    return render(request, 'interviews/interview_feedback.html', context)


@login_required(login_url='login')
@require_http_methods(['GET'])
def interview_history(request):
    """List the user's past interview sessions."""
    interviews = Interview.objects.filter(user=request.user).order_by('-created_at')
    average_score = interviews.aggregate(avg_score=Avg('overall_score')).get('avg_score') or 0

    context = {
        'interviews': interviews,
        'total_interviews': interviews.count(),
        'average_score': round(average_score),
        'recent_interviews': interviews[:5],
        'page_title': 'Interview History',
    }
    return render(request, 'interviews/interview_history.html', context)
