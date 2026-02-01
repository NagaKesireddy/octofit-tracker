from django.contrib import admin
from .models import Workout, WorkoutType, UserStats

@admin.register(WorkoutType)
class WorkoutTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_name', 'icon', 'default_calories_multiplier']
    search_fields = ['name', 'display_name']


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'workout_type', 'duration', 'distance', 'calories', 'created_at']
    list_filter = ['date', 'workout_type', 'created_at']
    search_fields = ['user__username', 'notes']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User & Date', {
            'fields': ('user', 'date')
        }),
        ('Workout Details', {
            'fields': ('workout_type', 'duration', 'distance', 'calories')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserStats)
class UserStatsAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_distance_7days', 'total_time_7days', 'total_distance_alltime', 'updated_at']
    list_filter = ['updated_at']
    search_fields = ['user__username']
    readonly_fields = ['updated_at']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('7-Day Statistics', {
            'fields': ('total_distance_7days', 'total_time_7days', 'workouts_count_7days')
        }),
        ('30-Day Statistics', {
            'fields': ('total_distance_30days', 'total_time_30days', 'workouts_count_30days')
        }),
        ('All-Time Statistics', {
            'fields': ('total_distance_alltime', 'total_time_alltime', 'workouts_count_alltime', 'total_calories_alltime')
        }),
        ('Metadata', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )
