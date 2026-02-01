"""
Test script to verify API endpoints with sample data
Run with: python manage.py shell < test_api.py
"""
import json
from django.test import Client
from django.contrib.auth.models import User

# Create test client
client = Client()

print("=" * 80)
print("TESTING OCTOFIT TRACKER API ENDPOINTS")
print("=" * 80)

# Get a test user for authentication
user = User.objects.first()
print(f"\nUsing test user: {user.username}")

# Login the user
client.force_login(user)

print("\n" + "=" * 80)
print("1. GET /api/workout-types/")
print("=" * 80)
response = client.get('/api/workout-types/')
print(f"Status: {response.status_code}")
print("Response:")
data = json.loads(response.content)
print(json.dumps(data, indent=2))

print("\n" + "=" * 80)
print("2. GET /api/workouts/")
print("=" * 80)
response = client.get('/api/workouts/')
print(f"Status: {response.status_code}")
print("Response:")
data = json.loads(response.content)
print(json.dumps(data, indent=2))

print("\n" + "=" * 80)
print("3. GET /api/workouts/statistics/")
print("=" * 80)
response = client.get('/api/workouts/statistics/')
print(f"Status: {response.status_code}")
print("Response:")
data = json.loads(response.content)
print(json.dumps(data, indent=2))

print("\n" + "=" * 80)
print("4. GET /api/stats/leaderboard_7days/")
print("=" * 80)
response = client.get('/api/stats/leaderboard_7days/')
print(f"Status: {response.status_code}")
print("Response:")
data = json.loads(response.content)
print(json.dumps(data, indent=2))

print("\n" + "=" * 80)
print("5. GET /api/stats/leaderboard_30days/")
print("=" * 80)
response = client.get('/api/stats/leaderboard_30days/')
print(f"Status: {response.status_code}")
print("Response:")
data = json.loads(response.content)
print(json.dumps(data, indent=2))

print("\n" + "=" * 80)
print("6. GET /api/stats/leaderboard_alltime/")
print("=" * 80)
response = client.get('/api/stats/leaderboard_alltime/')
print(f"Status: {response.status_code}")
print("Response:")
data = json.loads(response.content)
print(json.dumps(data, indent=2))

print("\n" + "=" * 80)
print("API ENDPOINT TESTING COMPLETE!")
print("=" * 80)
