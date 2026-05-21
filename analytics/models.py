from django.contrib.auth.models import User
from django.db import models
from django.db.models import JSONField
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


class WeakTopic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weak_topics')
    topic = models.CharField(max_length=128)
    severity = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    notes = models.TextField(blank=True)
    last_seen = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'topic')
        ordering = ['-severity', 'topic']

    def __str__(self):
        return f"Weak topic: {self.topic} ({self.severity}%)"


class StrongTopic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='strong_topics')
    topic = models.CharField(max_length=128)
    confidence = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    notes = models.TextField(blank=True)
    last_seen = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'topic')
        ordering = ['-confidence', 'topic']

    def __str__(self):
        return f"Strong topic: {self.topic} ({self.confidence}%)"


class AverageScore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='average_score')
    average_score = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    interview_count = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} average score: {self.average_score}%"


class InterviewStat(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='interview_stat')
    total_interviews = models.PositiveIntegerField(default=0)
    average_score = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    weak_topics = JSONField(default=list, blank=True)
    strong_topics = JSONField(default=list, blank=True)
    improvement_areas = JSONField(default=list, blank=True)
    trend_summary = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Interview stats for {self.user.username}"
