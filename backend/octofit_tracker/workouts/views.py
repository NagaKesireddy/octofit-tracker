from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Count

from .models import Workout, WorkoutType, UserStats
from django.contrib.auth.models import User
from .serializers import (
    WorkoutSerializer,
    WorkoutCreateUpdateSerializer,
    WorkoutTypeSerializer,
    UserStatsSerializer
)
from django.http import JsonResponse
from django.middleware.csrf import get_token


def csrf_token_view(request):
    """Return a fresh CSRF token in JSON (useful for SPA clients)."""
    token = get_token(request)
    return JsonResponse({'csrfToken': token})


class WorkoutViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Workout CRUD operations.
    Provides:
    - List all workouts for authenticated user
    - Create new workout
    - Retrieve, update, delete individual workouts
    """
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_fields = ['date', 'workout_type']
    search_fields = ['notes']
    ordering_fields = ['date', 'created_at']
    ordering = ['-date']
    
    def get_queryset(self):
        """Return only workouts for the authenticated user."""
        user = getattr(self.request, 'user', None)
        if not user or not user.is_authenticated:
            # For unauthenticated requests, return an empty queryset
            return Workout.objects.none()
        return Workout.objects.filter(user=user)
    
    def get_serializer_class(self):
        """Use different serializers for different actions."""
        if self.action in ['create', 'update', 'partial_update']:
            return WorkoutCreateUpdateSerializer
        return WorkoutSerializer
    
    def perform_create(self, serializer):
        """Automatically set the user to the authenticated user."""
        serializer.save(user=self.request.user)
        self._update_user_stats(self.request.user)
    
    def perform_update(self, serializer):
        """Update and recalculate stats."""
        serializer.save()
        self._update_user_stats(self.request.user)
    
    def perform_destroy(self, instance):
        """Delete and recalculate stats."""
        instance.delete()
        self._update_user_stats(self.request.user)
    
    @staticmethod
    def _update_user_stats(user):
        """Recalculate user stats based on workouts."""
        today = timezone.now().date()
        seven_days_ago = today - timedelta(days=7)
        thirty_days_ago = today - timedelta(days=30)
        
        # Calculate 7-day stats
        workouts_7days = Workout.objects.filter(
            user=user,
            date__gte=seven_days_ago
        )
        stats_7days = workouts_7days.aggregate(
            distance=Sum('distance'),
            time=Sum('duration'),
            count=Count('id')
        )
        
        # Calculate 30-day stats
        workouts_30days = Workout.objects.filter(
            user=user,
            date__gte=thirty_days_ago
        )
        stats_30days = workouts_30days.aggregate(
            distance=Sum('distance'),
            time=Sum('duration'),
            count=Count('id')
        )
        
        # Calculate all-time stats
        all_workouts = Workout.objects.filter(user=user)
        stats_alltime = all_workouts.aggregate(
            distance=Sum('distance'),
            time=Sum('duration'),
            count=Count('id'),
            calories=Sum('calories')
        )
        
        # Update or create UserStats
        user_stats, _ = UserStats.objects.get_or_create(user=user)
        user_stats.total_distance_7days = stats_7days['distance'] or 0.0
        user_stats.total_time_7days = stats_7days['time'] or 0
        user_stats.workouts_count_7days = stats_7days['count'] or 0
        
        user_stats.total_distance_30days = stats_30days['distance'] or 0.0
        user_stats.total_time_30days = stats_30days['time'] or 0
        user_stats.workouts_count_30days = stats_30days['count'] or 0
        
        user_stats.total_distance_alltime = stats_alltime['distance'] or 0.0
        user_stats.total_time_alltime = stats_alltime['time'] or 0
        user_stats.workouts_count_alltime = stats_alltime['count'] or 0
        user_stats.total_calories_alltime = stats_alltime['calories'] or 0
        
        user_stats.save()
    
    @action(detail=False, methods=['get'])
    def by_date(self, request):
        """Filter workouts by date range."""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        queryset = self.get_queryset()
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get workout statistics for the authenticated user."""
        try:
            stats = UserStats.objects.get(user=request.user)
            serializer = UserStatsSerializer(stats)
            return Response(serializer.data)
        except UserStats.DoesNotExist:
            return Response(
                {'detail': 'No statistics found for this user.'},
                status=status.HTTP_404_NOT_FOUND
            )


class WorkoutTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for WorkoutType (read-only).
    Lists available workout types.
    """
    queryset = WorkoutType.objects.all()
    serializer_class = WorkoutTypeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserStatsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for UserStats (read-only).
    Provides leaderboard data and user statistics.
    """
    serializer_class = UserStatsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """Return stats, optionally filtered by period."""
        return UserStats.objects.all()
    
    @action(detail=False, methods=['get'])
    def my_stats(self, request):
        """Get stats for the authenticated user."""
        try:
            stats = UserStats.objects.get(user=request.user)
            serializer = self.get_serializer(stats)
            return Response(serializer.data)
        except UserStats.DoesNotExist:
            return Response(
                {'detail': 'No statistics found for this user.'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def leaderboard_7days(self, request):
        """Get leaderboard for top distance in last 7 days."""
        limit = int(request.query_params.get('limit', 10))
        leaderboard = UserStats.objects.order_by(
            '-total_distance_7days'
        )[:limit]
        serializer = self.get_serializer(leaderboard, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def leaderboard_30days(self, request):
        """Get leaderboard for top distance in last 30 days."""
        limit = int(request.query_params.get('limit', 10))
        leaderboard = UserStats.objects.order_by(
            '-total_distance_30days'
        )[:limit]
        serializer = self.get_serializer(leaderboard, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def leaderboard_alltime(self, request):
        """Get all-time leaderboard."""
        limit = int(request.query_params.get('limit', 10))
        leaderboard = UserStats.objects.order_by(
            '-total_distance_alltime'
        )[:limit]
        serializer = self.get_serializer(leaderboard, many=True)
        return Response(serializer.data)
