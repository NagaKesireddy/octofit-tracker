"""
URL configuration for octofit_tracker project.
"""
import os
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from workouts.views import WorkoutViewSet, WorkoutTypeViewSet, UserStatsViewSet, csrf_token_view

# Initialize router for API endpoints
router = DefaultRouter()
router.register(r'workouts', WorkoutViewSet, basename='workout')
router.register(r'workout-types', WorkoutTypeViewSet, basename='workout-type')
router.register(r'stats', UserStatsViewSet, basename='stats')

# Codespace environment-aware URL configuration
codespace_name = os.environ.get('CODESPACE_NAME')
if codespace_name:
    base_url = f"https://{codespace_name}-8000.app.github.dev"
else:
    base_url = "http://localhost:8000"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/csrf/', csrf_token_view),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
