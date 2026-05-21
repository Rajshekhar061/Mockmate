from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Avg


class Interview(models.Model):
    """Stores metadata for a mock interview session."""

    ROLE_CHOICES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('fullstack', 'Fullstack'),
        ('django', 'Django'),
        ('dsa', 'DSA'),
        ('hr', 'HR'),
    ]

    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    INTERVIEW_TYPE_CHOICES = [
        ('technical', 'Technical'),
        ('behavioral', 'Behavioral'),
        ('hr', 'HR'),
        ('soft_skills', 'Soft Skills'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interviews')
    role = models.CharField(max_length=32, choices=ROLE_CHOICES)
    difficulty = models.CharField(max_length=16, choices=DIFFICULTY_CHOICES)
    interview_type = models.CharField(max_length=24, choices=INTERVIEW_TYPE_CHOICES)
    overall_score = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_role_display()} interview ({self.get_difficulty_display()})"

    def completed_questions(self):
        return self.questions.exclude(user_answer__exact='').count()

    def question_count(self):
        return self.questions.count()

    def is_complete(self):
        return self.question_count() > 0 and self.completed_questions() == self.question_count()

    def calculate_overall_score(self):
        average = self.questions.aggregate(avg_score=Avg('score')).get('avg_score') or 0
        self.overall_score = round(average)
        self.save(update_fields=['overall_score'])


class InterviewQuestion(models.Model):
    """A single question within a mock interview session."""

    interview = models.ForeignKey(
        Interview,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    order = models.PositiveIntegerField(default=1)
    question = models.TextField()
    user_answer = models.TextField(blank=True)
    ai_feedback = models.TextField(blank=True)
    score = models.IntegerField(default=0)
    ideal_answer = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        unique_together = ('interview', 'order')

    def __str__(self):
        return f"Question {self.order} for Interview {self.interview_id}"
