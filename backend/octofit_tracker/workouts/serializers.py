from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Workout, WorkoutType, UserStats

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class WorkoutTypeSerializer(serializers.ModelSerializer):
    """Serializer for WorkoutType model."""
    class Meta:
        model = WorkoutType
        fields = ['id', 'name', 'display_name', 'icon', 'default_calories_multiplier']
        read_only_fields = ['id']


class WorkoutSerializer(serializers.ModelSerializer):
    """Serializer for Workout model."""
    user = UserSerializer(read_only=True)
    workout_type_display = serializers.CharField(
        source='get_workout_type_display',
        read_only=True
    )
    
    class Meta:
        model = Workout
        fields = [
            'id',
            'user',
            'date',
            'workout_type',
            'workout_type_display',
            'duration',
            'distance',
            'calories',
            'notes',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'workout_type_display']


class WorkoutCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating workouts (without nested user)."""
    class Meta:
        model = Workout
        fields = [
            'date',
            'workout_type',
            'duration',
            'distance',
            'calories',
            'notes'
        ]


class UserStatsSerializer(serializers.ModelSerializer):
    """Serializer for UserStats model."""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserStats
        fields = [
            'id',
            'user',
            'total_distance_7days',
            'total_time_7days',
            'workouts_count_7days',
            'total_distance_30days',
            'total_time_30days',
            'workouts_count_30days',
            'total_distance_alltime',
            'total_time_alltime',
            'workouts_count_alltime',
            'total_calories_alltime',
            'updated_at'
        ]
        read_only_fields = fields
