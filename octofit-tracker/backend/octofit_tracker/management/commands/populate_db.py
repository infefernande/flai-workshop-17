from django.core.management.base import BaseCommand
from api.models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing data...')
        
        # Delete all existing data using Django ORM
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('Existing data cleared.'))
        
        # Create Teams
        self.stdout.write('Creating teams...')
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='Mightiest Heroes of the Marvel Universe',
            members_count=6
        )
        
        team_dc = Team.objects.create(
            name='Team DC',
            description='Justice League - DC Universe Heroes',
            members_count=6
        )
        
        self.stdout.write(self.style.SUCCESS(f'Created {Team.objects.count()} teams.'))
        
        # Create Users - Marvel Heroes
        self.stdout.write('Creating users...')
        marvel_users = [
            {'name': 'Iron Man', 'email': 'tony.stark@marvel.com', 'fitness_level': 'Advanced'},
            {'name': 'Captain America', 'email': 'steve.rogers@marvel.com', 'fitness_level': 'Expert'},
            {'name': 'Thor', 'email': 'thor.odinson@marvel.com', 'fitness_level': 'Godly'},
            {'name': 'Black Widow', 'email': 'natasha.romanoff@marvel.com', 'fitness_level': 'Expert'},
            {'name': 'Hulk', 'email': 'bruce.banner@marvel.com', 'fitness_level': 'Extreme'},
            {'name': 'Spider-Man', 'email': 'peter.parker@marvel.com', 'fitness_level': 'Advanced'},
        ]
        
        # Create Users - DC Heroes
        dc_users = [
            {'name': 'Superman', 'email': 'clark.kent@dc.com', 'fitness_level': 'Godly'},
            {'name': 'Batman', 'email': 'bruce.wayne@dc.com', 'fitness_level': 'Expert'},
            {'name': 'Wonder Woman', 'email': 'diana.prince@dc.com', 'fitness_level': 'Godly'},
            {'name': 'Flash', 'email': 'barry.allen@dc.com', 'fitness_level': 'Advanced'},
            {'name': 'Aquaman', 'email': 'arthur.curry@dc.com', 'fitness_level': 'Advanced'},
            {'name': 'Green Lantern', 'email': 'hal.jordan@dc.com', 'fitness_level': 'Expert'},
        ]
        
        created_users = []
        for user_data in marvel_users:
            user = User.objects.create(
                name=user_data['name'],
                email=user_data['email'],
                team='Team Marvel',
                fitness_level=user_data['fitness_level']
            )
            created_users.append(user)
        
        for user_data in dc_users:
            user = User.objects.create(
                name=user_data['name'],
                email=user_data['email'],
                team='Team DC',
                fitness_level=user_data['fitness_level']
            )
            created_users.append(user)
        
        self.stdout.write(self.style.SUCCESS(f'Created {User.objects.count()} users.'))
        
        # Create Activities
        self.stdout.write('Creating activities...')
        activity_types = ['Running', 'Swimming', 'Cycling', 'Weight Training', 'Boxing', 'Yoga', 'HIIT']
        
        for user in created_users:
            # Create 5-10 activities per user
            num_activities = random.randint(5, 10)
            for i in range(num_activities):
                activity_type = random.choice(activity_types)
                duration = random.randint(20, 120)
                calories = duration * random.randint(5, 12)
                distance = round(random.uniform(2, 20), 2) if activity_type in ['Running', 'Cycling', 'Swimming'] else None
                
                Activity.objects.create(
                    user_id=user.id,
                    user_name=user.name,
                    activity_type=activity_type,
                    duration=duration,
                    calories_burned=calories,
                    distance=distance,
                    date=datetime.now() - timedelta(days=random.randint(0, 30)),
                    notes=f'{activity_type} session'
                )
        
        self.stdout.write(self.style.SUCCESS(f'Created {Activity.objects.count()} activities.'))
        
        # Create Leaderboard entries
        self.stdout.write('Creating leaderboard...')
        leaderboard_data = []
        
        for user in created_users:
            user_activities = Activity.objects.filter(user_id=user.id)
            total_calories = sum(activity.calories_burned for activity in user_activities)
            total_activities = user_activities.count()
            total_distance = sum(activity.distance for activity in user_activities if activity.distance)
            
            leaderboard_data.append({
                'user_id': user.id,
                'user_name': user.name,
                'team': user.team,
                'total_calories': total_calories,
                'total_activities': total_activities,
                'total_distance': round(total_distance, 2)
            })
        
        # Sort by total calories and assign ranks
        leaderboard_data.sort(key=lambda x: x['total_calories'], reverse=True)
        
        for rank, data in enumerate(leaderboard_data, start=1):
            Leaderboard.objects.create(
                user_id=data['user_id'],
                user_name=data['user_name'],
                team=data['team'],
                total_calories=data['total_calories'],
                total_activities=data['total_activities'],
                total_distance=data['total_distance'],
                rank=rank
            )
        
        self.stdout.write(self.style.SUCCESS(f'Created {Leaderboard.objects.count()} leaderboard entries.'))
        
        # Create Workouts
        self.stdout.write('Creating workouts...')
        workouts = [
            {
                'name': 'Super Soldier Training',
                'description': 'Captain America\'s legendary training routine',
                'difficulty': 'Expert',
                'duration': 90,
                'calories_estimate': 850,
                'exercises': ['Push-ups', 'Pull-ups', 'Shield throws', 'Combat drills'],
                'target_muscle_groups': ['Chest', 'Back', 'Arms', 'Core'],
                'equipment_needed': ['Pull-up bar', 'Shield', 'Weights']
            },
            {
                'name': 'Asgardian Warrior Workout',
                'description': 'Thor\'s godly strength training',
                'difficulty': 'Godly',
                'duration': 120,
                'calories_estimate': 1200,
                'exercises': ['Hammer swings', 'Battle rope', 'Heavy squats', 'Thunder claps'],
                'target_muscle_groups': ['Full body', 'Core', 'Legs', 'Shoulders'],
                'equipment_needed': ['Battle rope', 'Heavy weights', 'Hammer']
            },
            {
                'name': 'Spider Agility Training',
                'description': 'Spider-Man\'s acrobatic workout',
                'difficulty': 'Advanced',
                'duration': 60,
                'calories_estimate': 600,
                'exercises': ['Web swings', 'Wall climbs', 'Plyometrics', 'Parkour'],
                'target_muscle_groups': ['Legs', 'Core', 'Arms', 'Back'],
                'equipment_needed': ['Climbing wall', 'Gymnastic rings']
            },
            {
                'name': 'Kryptonian Power Circuit',
                'description': 'Superman\'s maximum strength routine',
                'difficulty': 'Godly',
                'duration': 90,
                'calories_estimate': 1100,
                'exercises': ['Heavy lifts', 'Flight simulation', 'Heat vision focus', 'Speed drills'],
                'target_muscle_groups': ['Full body', 'Core', 'Legs'],
                'equipment_needed': ['Maximum weights', 'Speed track']
            },
            {
                'name': 'Dark Knight Conditioning',
                'description': 'Batman\'s tactical fitness program',
                'difficulty': 'Expert',
                'duration': 75,
                'calories_estimate': 750,
                'exercises': ['Martial arts', 'Rope climbing', 'Grappling', 'Stealth training'],
                'target_muscle_groups': ['Full body', 'Core', 'Flexibility'],
                'equipment_needed': ['Martial arts gear', 'Grappling equipment']
            },
            {
                'name': 'Amazon Warrior Training',
                'description': 'Wonder Woman\'s legendary combat workout',
                'difficulty': 'Godly',
                'duration': 100,
                'calories_estimate': 950,
                'exercises': ['Sword combat', 'Shield defense', 'Lasso drills', 'Combat rolls'],
                'target_muscle_groups': ['Full body', 'Arms', 'Core', 'Legs'],
                'equipment_needed': ['Sword', 'Shield', 'Lasso', 'Training dummy']
            },
            {
                'name': 'Speed Force Cardio',
                'description': 'Flash\'s ultra-fast cardio routine',
                'difficulty': 'Advanced',
                'duration': 45,
                'calories_estimate': 800,
                'exercises': ['Sprint intervals', 'Quick feet drills', 'Reaction training'],
                'target_muscle_groups': ['Legs', 'Cardio', 'Core'],
                'equipment_needed': ['Track', 'Agility ladder', 'Reaction lights']
            },
            {
                'name': 'Gamma Strength Protocol',
                'description': 'Hulk\'s maximum strength building',
                'difficulty': 'Extreme',
                'duration': 60,
                'calories_estimate': 1000,
                'exercises': ['Heavy deadlifts', 'Smash training', 'Rage focus', 'Boulder throws'],
                'target_muscle_groups': ['Full body', 'Legs', 'Back', 'Shoulders'],
                'equipment_needed': ['Maximum weights', 'Heavy objects']
            },
        ]
        
        for workout_data in workouts:
            Workout.objects.create(**workout_data)
        
        self.stdout.write(self.style.SUCCESS(f'Created {Workout.objects.count()} workouts.'))
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n=== Database Population Complete ==='))
        self.stdout.write(self.style.SUCCESS(f'Teams: {Team.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Users: {User.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Activities: {Activity.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Leaderboard entries: {Leaderboard.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Workouts: {Workout.objects.count()}'))
