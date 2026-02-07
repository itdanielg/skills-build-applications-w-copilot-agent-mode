from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        app_label = 'octofit_tracker'

class Activity(models.Model):
    name = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    class Meta:
        app_label = 'octofit_tracker'

class Leaderboard(models.Model):
    team = models.CharField(max_length=100)
    points = models.IntegerField()
    class Meta:
        app_label = 'octofit_tracker'

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    class Meta:
        app_label = 'octofit_tracker'

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        User = get_user_model()
        # Delete existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create users
        users = [
            {'email': 'ironman@marvel.com', 'username': 'IronMan', 'team': 'Marvel'},
            {'email': 'captain@marvel.com', 'username': 'CaptainAmerica', 'team': 'Marvel'},
            {'email': 'batman@dc.com', 'username': 'Batman', 'team': 'DC'},
            {'email': 'superman@dc.com', 'username': 'Superman', 'team': 'DC'},
        ]
        for u in users:
            User.objects.create_user(email=u['email'], username=u['username'], password='password')

        # Create activities
        Activity.objects.create(name='Running', user='IronMan', team='Marvel')
        Activity.objects.create(name='Swimming', user='CaptainAmerica', team='Marvel')
        Activity.objects.create(name='Cycling', user='Batman', team='DC')
        Activity.objects.create(name='Flying', user='Superman', team='DC')

        # Create leaderboard
        Leaderboard.objects.create(team='Marvel', points=100)
        Leaderboard.objects.create(team='DC', points=90)

        # Create workouts
        Workout.objects.create(name='Hero Training', description='Intense workout for superheroes.')
        Workout.objects.create(name='Power Up', description='Strength and endurance training.')

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
