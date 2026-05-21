from django.contrib import admin
from .models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    """
    Admin configuration for Resume model.
    """
    list_display = [
        'original_filename',
        'user',
        'ats_score',
        'status',
        'created_at',
        'analyzed_at',
    ]
    list_filter = ['status', 'created_at', 'ats_score']
    search_fields = ['original_filename', 'user__username', 'user__email']
    readonly_fields = [
        'extracted_text',
        'ats_score',
        'strengths',
        'weaknesses',
        'suggestions',
        'analysis_details',
        'keywords_found',
        'created_at',
        'updated_at',
        'analyzed_at',
    ]
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'original_filename'),
        }),
        ('File Information', {
            'fields': ('uploaded_file', 'extracted_text'),
        }),
        ('Analysis Results', {
            'fields': (
                'ats_score',
                'strengths',
                'weaknesses',
                'suggestions',
                'keywords_found',
                'analysis_details',
            ),
        }),
        ('Status', {
            'fields': ('status', 'error_message'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'analyzed_at'),
            'classes': ('collapse',),
        }),
    )
    
    def has_add_permission(self, request):
        """Disable adding resumes from admin."""
        return False
