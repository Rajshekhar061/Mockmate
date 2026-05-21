from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
import json


class Resume(models.Model):
    """
    Resume model for storing user resume uploads and AI analysis results.
    """
    STATUS_CHOICES = [
        ('uploaded', 'Uploaded'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    # Relations
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')

    # File Information
    uploaded_file = models.FileField(
        upload_to='resumes/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text='PDF resume file (max 5MB)'
    )
    original_filename = models.CharField(max_length=255, blank=True)

    # Content
    extracted_text = models.TextField(blank=True, null=True, help_text='Extracted text from PDF')

    # Analysis Results (JSON fields for flexibility)
    ats_score = models.IntegerField(null=True, blank=True, help_text='ATS score (0-100)')
    strengths = models.JSONField(default=list, blank=True, help_text='List of resume strengths')
    weaknesses = models.JSONField(default=list, blank=True, help_text='List of resume weaknesses')
    suggestions = models.JSONField(default=list, blank=True, help_text='Improvement suggestions')
    analysis_details = models.JSONField(default=dict, blank=True, help_text='Full analysis details')

    # Keywords and Metrics
    keywords_found = models.JSONField(default=list, blank=True, help_text='Keywords found in resume')
    job_match_score = models.IntegerField(null=True, blank=True, help_text='Job match percentage')

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='uploaded')
    error_message = models.TextField(blank=True, null=True, help_text='Error details if analysis failed')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    analyzed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Resume'
        verbose_name_plural = 'Resumes'
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.original_filename or self.uploaded_file.name}"

    def get_strengths_list(self):
        """Get strengths as a list"""
        if isinstance(self.strengths, list):
            return self.strengths
        return json.loads(self.strengths) if self.strengths else []

    def get_weaknesses_list(self):
        """Get weaknesses as a list"""
        if isinstance(self.weaknesses, list):
            return self.weaknesses
        return json.loads(self.weaknesses) if self.weaknesses else []

    def get_suggestions_list(self):
        """Get suggestions as a list"""
        if isinstance(self.suggestions, list):
            return self.suggestions
        return json.loads(self.suggestions) if self.suggestions else []

    def is_analyzed(self):
        """Check if resume has been analyzed"""
        return self.status == 'completed' and self.ats_score is not None

    def get_analysis_summary(self):
        """Get a summary of the analysis"""
        return {
            'ats_score': self.ats_score,
            'status': self.status,
            'strengths_count': len(self.get_strengths_list()),
            'weaknesses_count': len(self.get_weaknesses_list()),
            'suggestions_count': len(self.get_suggestions_list()),
        }

