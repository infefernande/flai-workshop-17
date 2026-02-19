from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'team', 'fitness_level', 'created_at']


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'created_at', 'members_count']


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'user_id', 'user_name', 'activity_type', 'duration', 
                  'calories_burned', 'distance', 'date', 'notes']


class LeaderboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaderboard
        fields = ['id', 'user_id', 'user_name', 'team', 'total_calories', 
                  'total_activities', 'total_distance', 'rank', 'last_updated']


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['id', 'name', 'description', 'difficulty', 'duration', 
                  'calories_estimate', 'exercises', 'target_muscle_groups', 'equipment_needed']
