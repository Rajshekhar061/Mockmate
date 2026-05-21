from django.urls import path
from . import views

urlpatterns = [
    path('', views.insights, name='analytics_insights'),
]
