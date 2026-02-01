from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random
from workouts.models import Workout, WorkoutType, UserStats


class Command(BaseCommand):
    help = 'Populate the database with sample fitness data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Starting to populate sample data...')
        
        # Create WorkoutTypes
        self.stdout.write('Creating workout types...')
        workout_types_data = [
            {'name': 'run', 'display_name': 'Running', 'icon': '🏃', 'default_calories_multiplier': 1.0},
            {'name': 'walk', 'display_name': 'Walking', 'icon': '🚶', 'default_calories_multiplier': 0.5},
            {'name': 'cycling', 'display_name': 'Cycling', 'icon': '🚴', 'default_calories_multiplier': 0.8},
            {'name': 'gym', 'display_name': 'Gym', 'icon': '💪', 'default_calories_multiplier': 1.2},
        ]
        
        for wt_data in workout_types_data:
            WorkoutType.objects.get_or_create(
                name=wt_data['name'],
                defaults={
                    'display_name': wt_data['display_name'],
                    'icon': wt_data['icon'],
                    'default_calories_multiplier': wt_data['default_calories_multiplier'],
                }
            )
        self.stdout.write(self.style.SUCCESS('✓ Workout types created'))
        
        # Create sample users
        self.stdout.write('Creating sample users...')
        users_data = [
            {'username': 'alice_runner', 'email': 'alice@example.com', 'first_name': 'Alice', 'last_name': 'Runner'},
            {'username': 'bob_cyclist', 'email': 'bob@example.com', 'first_name': 'Bob', 'last_name': 'Cyclist'},
            {'username': 'charlie_gym', 'email': 'charlie@example.com', 'first_name': 'Charlie', 'last_name': 'Gym'},
        ]
        
        users = {}
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                }
            )
            users[user_data['username']] = user
            if created:
                self.stdout.write(f'  Created user: {user_data["username"]}')
        
        self.stdout.write(self.style.SUCCESS('✓ Sample users created/verified'))
        
        # Create sample workouts
        self.stdout.write('Creating sample workouts...')
        today = timezone.now().date()
        workouts_created = 0
        
        # Define workout templates for each user
        user_workouts = {
            'alice_runner': [
                {'type': 'run', 'duration': 30, 'distance': 5.0, 'calories': 350},
                {'type': 'run', 'duration': 45, 'distance': 8.0, 'calories': 550},
                {'type': 'walk', 'duration': 60, 'distance': 5.0, 'calories': 250},
            ],
            'bob_cyclist': [
                {'type': 'cycling', 'duration': 60, 'distance': 20.0, 'calories': 500},
                {'type': 'cycling', 'duration': 90, 'distance': 35.0, 'calories': 750},
                {'type': 'gym', 'duration': 45, 'distance': 0.0, 'calories': 400},
            ],
            'charlie_gym': [
                {'type': 'gym', 'duration': 60, 'distance': 0.0, 'calories': 450},
                {'type': 'gym', 'duration': 75, 'distance': 0.0, 'calories': 550},
                {'type': 'walk', 'duration': 45, 'distance': 3.5, 'calories': 200},
            ],
        }
        
        # Generate workouts for the last 30 days
        for username, user in users.items():
            templates = user_workouts[username]
            
            # Create 8-12 workouts per user over the last 30 days
            num_workouts = random.randint(8, 12)
            for _ in range(num_workouts):
                days_ago = random.randint(0, 29)
                workout_date = today - timedelta(days=days_ago)
                
                template = random.choice(templates)
                
                # Add some variation to the template
                duration = template['duration'] + random.randint(-10, 10)
                distance = template['distance'] + random.uniform(-1.0, 1.0)
                distance = max(0, distance)  # Ensure non-negative
                calories = template['calories'] + random.randint(-50, 50)
                calories = max(0, calories)  # Ensure non-negative
                
                notes = random.choice([
                    'Great workout!',
                    'Feeling energized',
                    'Morning session',
                    'Evening run',
                    'Pushing harder',
                    'Recovery day',
                    'New personal best!',
                    None
                ])
                
                Workout.objects.create(
                    user=user,
                    date=workout_date,
                    workout_type=template['type'],
                    duration=max(1, duration),
                    distance=distance,
                    calories=int(calories),
                    notes=notes
                )
                workouts_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {workouts_created} sample workouts'))
        
        # Recalculate UserStats for all users
        self.stdout.write('Calculating user statistics...')
        for user in users.values():
            self._update_user_stats(user)
        
        self.stdout.write(self.style.SUCCESS('✓ User statistics calculated'))
        
        # Display summary
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('Sample Data Population Complete!'))
        self.stdout.write('='*60)
        
        for username, user in users.items():
            try:
                stats = UserStats.objects.get(user=user)
                self.stdout.write(f'\n{user.first_name} {user.last_name} ({username}):')
                self.stdout.write(f'  7-day:    {stats.total_distance_7days:.1f}km, {stats.total_time_7days}min, {stats.workouts_count_7days} workouts')
                self.stdout.write(f'  30-day:   {stats.total_distance_30days:.1f}km, {stats.total_time_30days}min, {stats.workouts_count_30days} workouts')
                self.stdout.write(f'  All-time: {stats.total_distance_alltime:.1f}km, {stats.total_time_alltime}min, {stats.workouts_count_alltime} workouts, {stats.total_calories_alltime} cal')
            except UserStats.DoesNotExist:
                self.stdout.write(f'  No stats found for {username}')
    
    @staticmethod
    def _update_user_stats(user):
        """Recalculate user stats based on workouts."""
        from django.db.models import Sum, Count
        
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
