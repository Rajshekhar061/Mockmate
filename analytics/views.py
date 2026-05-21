import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .services import AnalyticsService

logger = logging.getLogger(__name__)


@login_required(login_url='login')
def insights(request):
    analytics_context = AnalyticsService(request.user).refresh_user_analytics()

    context = {
        'analytics': analytics_context,
        'page_title': 'Analytics Insights',
    }
    return render(request, 'analytics/overview.html', context)
