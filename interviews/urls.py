from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start_interview, name='start_interview'),
    path('history/', views.interview_history, name='interview_history'),
    path('<int:interview_id>/question/<int:question_index>/', views.interview_question, name='interview_question'),
    path('<int:interview_id>/feedback/', views.interview_feedback, name='interview_feedback'),
]
