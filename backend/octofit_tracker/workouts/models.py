from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone

class WorkoutType(models.Model):
    """Reference model for workout types."""
    WORKOUT_CHOICES = [
        ('run', 'Running'),
        ('walk', 'Walking'),
        ('cycling', 'Cycling'),
        ('gym', 'Gym'),
    ]
    
    name = models.CharField(
        max_length=50,
        choices=WORKOUT_CHOICES,
        unique=True
    )
    display_name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, default='💪')
    default_calories_multiplier = models.FloatField(default=1.0)
    
    class Meta:
        verbose_name_plural = "Workout Types"
        ordering = ['name']
    
    def __str__(self):
        return self.display_name


class Workout(models.Model):
    """Model for logging individual workouts."""
    WORKOUT_CHOICES = [
        ('run', 'Running'),
        ('walk', 'Walking'),
        ('cycling', 'Cycling'),
        ('gym', 'Gym'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='workouts'
    )
    date = models.DateField(default=timezone.now)
    workout_type = models.CharField(
        max_length=20,
        choices=WORKOUT_CHOICES
    )
    duration = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text='Duration in minutes'
    )
    distance = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text='Distance in kilometers'
    )
    calories = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        help_text='Calories burned'
    )
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', '-date']),
            models.Index(fields=['user', 'workout_type']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.get_workout_type_display()} on {self.date}"


class UserStats(models.Model):
    """Aggregated statistics for leaderboards (denormalized for performance)."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='stats'
    )
    
    # 7-day stats
    total_distance_7days = models.FloatField(default=0.0)
    total_time_7days = models.PositiveIntegerField(default=0)  # in minutes
    workouts_count_7days = models.PositiveIntegerField(default=0)
    
    # 30-day stats
    total_distance_30days = models.FloatField(default=0.0)
    total_time_30days = models.PositiveIntegerField(default=0)  # in minutes
    workouts_count_30days = models.PositiveIntegerField(default=0)
    
    # All-time stats
    total_distance_alltime = models.FloatField(default=0.0)
    total_time_alltime = models.PositiveIntegerField(default=0)  # in minutes
    workouts_count_alltime = models.PositiveIntegerField(default=0)
    total_calories_alltime = models.PositiveIntegerField(default=0)
    
    # Tracking
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "User Stats"
    
    def __str__(self):
        return f"Stats for {self.user.username}"
