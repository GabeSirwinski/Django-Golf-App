from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Player(models.Model):
    player_name = models.CharField(max_length=60)
    average_score = models.IntegerField(validators=[MinValueValidator(0, message='This field can\'t be negative!'), MaxValueValidator(150)])
    driving_distance = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(500)])
    wins = models.PositiveIntegerField(default=0)
    player = models.Manager()

    def __str__(self):
        return self.player_name

class Tournament(models.Model):
    tournament_name = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    country = models.CharField(max_length=60)
    par = models.IntegerField(default=72)
    date = models.DateTimeField()
    winner = models.ForeignKey(Player, on_delete=models.CASCADE)
    tournament = models.Manager()

    def __str__(self):
        return self.tournament_name

class Favorite(models.Model):
    player_name = models.CharField(max_length=60)
    picture = models.CharField(max_length=300)
    pga_debut = models.CharField(max_length=60)
    college = models.CharField(max_length=60)
    country = models.CharField(max_length=60)
    college = models.CharField(max_length=60)
    born = models.CharField(max_length=60)
    favorite = models.Manager()

    def __str__(self):
        return self.player_name

