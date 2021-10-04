from django.db import models
from django.db.models.fields import related

# Create your models here.
class Team(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=3)

    def __str__(self) -> str:
        return self.name

class Game(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_team')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_team')
    date = models.DateField()

    def __str__(self) -> str:
        return f'{self.home_team.name} VS {self.away_team.name}'

class Player(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class Stats(models.Model):
    games = models.ManyToManyField(Game)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    points = models.PositiveSmallIntegerField()
    rebounds = models.PositiveSmallIntegerField()
    assists = models.PositiveSmallIntegerField()
    blocks = models.PositiveSmallIntegerField()

    free_throws_attempts = models.PositiveSmallIntegerField()
    free_throws_made = models.PositiveSmallIntegerField()
    free_throws_percent = models.FloatField()
    
    field_goals_attempts = models.PositiveSmallIntegerField()
    field_goals_made = models.PositiveSmallIntegerField()
    field_goals_percent = models.FloatField()