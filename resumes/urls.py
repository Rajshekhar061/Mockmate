from django.urls import path
from . import views

urlpatterns = [
    # Resume management
    path('upload/', views.upload_resume, name='upload_resume'),
    path('list/', views.resume_list, name='resume_list'),
    path('feedback/<int:resume_id>/', views.resume_feedback, name='resume_feedback'),
    path('delete/<int:resume_id>/', views.delete_resume, name='delete_resume'),
    path('reanalyze/<int:resume_id>/', views.reanalyze_resume, name='reanalyze_resume'),
    path('feedback/<int:resume_id>/', views.resume_feedback, name='resume_feedback'),
    path('list/', views.resume_list, name='resume_list'),
    path('delete/<int:resume_id>/', views.delete_resume, name='delete_resume'),
    path('reanalyze/<int:resume_id>/', views.reanalyze_resume, name='reanalyze_resume'),
]
