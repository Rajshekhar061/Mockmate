from django.contrib import admin

from .models import Interview, InterviewQuestion

@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'difficulty', 'interview_type', 'overall_score', 'created_at')
    list_filter = ('role', 'difficulty', 'interview_type')
    search_fields = ('user__username', 'role', 'interview_type')

@admin.register(InterviewQuestion)
class InterviewQuestionAdmin(admin.ModelAdmin):
    list_display = ('interview', 'order', 'score', 'created_at')
    list_filter = ('order',)
    search_fields = ('question', 'user_answer')
