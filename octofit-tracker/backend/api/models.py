from django.db import models
from django.contrib.auth.models import AbstractUser


class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    team = models.CharField(max_length=100)
    fitness_level = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    members_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'teams'

    def __str__(self):
        return self.name


class Activity(models.Model):
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=200)
    activity_type = models.CharField(max_length=100)
    duration = models.IntegerField()  # in minutes
    calories_burned = models.IntegerField()
    distance = models.FloatField(null=True, blank=True)  # in km
    date = models.DateTimeField()
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'activities'

    def __str__(self):
        return f"{self.user_name} - {self.activity_type}"


class Leaderboard(models.Model):
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=200)
    team = models.CharField(max_length=100)
    total_calories = models.IntegerField()
    total_activities = models.IntegerField()
    total_distance = models.FloatField()
    rank = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'leaderboard'
        ordering = ['rank']

    def __str__(self):
        return f"#{self.rank} - {self.user_name}"


class Workout(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=50)
    duration = models.IntegerField()  # in minutes
    calories_estimate = models.IntegerField()
    exercises = models.JSONField()  # List of exercises
    target_muscle_groups = models.JSONField()  # List of muscle groups
    equipment_needed = models.JSONField()  # List of equipment

    class Meta:
        db_table = 'workouts'

    def __str__(self):
        return self.name
