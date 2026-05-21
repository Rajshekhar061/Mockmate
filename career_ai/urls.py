"""
URL configuration for career_ai project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    
    # App URLs
    path("auth/", include("users.urls")),
    path("resume/", include("resumes.urls")),
    path("interviews/", include("interviews.urls")),
    path("analytics/", include("analytics.urls")),
    
    # Home
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
