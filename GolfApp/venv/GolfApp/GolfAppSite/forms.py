from django import forms
from .models import Player, Tournament
from django.core.validators import MaxValueValidator, MinValueValidator

class PlayerForm(forms.ModelForm):
    player_name = forms.CharField()
    average_score = forms.IntegerField(validators=[MinValueValidator(0, message='This field can\'t be negative!'), MaxValueValidator(150)])
    wins = forms.IntegerField()
    driving_distance = forms.IntegerField()
    class Meta:
        model = Player
        fields = "__all__"

class TournamentForm(forms.ModelForm):
    tournament_name = forms.CharField()
    city = forms.CharField()
    country = forms.CharField()
    date = forms.DateField()
    par = forms.IntegerField()
    winner = forms.ModelChoiceField(queryset=Player.player.all())
    class Meta:
        model = Tournament
        fields = "__all__"