from django.shortcuts import render, redirect, get_object_or_404
from .forms import PlayerForm, TournamentForm
from .models import Player, Tournament, Favorite
import requests, json
from bs4 import BeautifulSoup

def home(request):
    return render(request, 'GolfApp/home.html')

def create_new_player(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/Players')
        else:
            errors = "Please ensure the form is filled out properly (positive numbers only)"
            form = PlayerForm()
            return render(request, 'GolfApp/createPlayer.html', {'form': form, 'errors': errors})
    else:
        form = PlayerForm()
    return render(request, 'GolfApp/createPlayer.html', {'form': form})

def create_new_tournament(request):
    if request.method == 'POST':
        form = TournamentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/Tournaments')
    else:
        form = TournamentForm()
    return render(request, 'GolfApp/createTournament.html', {'form': form})

def index(request):
    players = Player.player.all()
    return render(request, 'GolfApp/playerIndex.html', {'players': players})

def details(request,pk):
    pk = int(pk)
    player_details = Player.player.get(id=pk)
    return render(request, 'GolfApp/playerDetails.html', {'player_details': player_details})

def tournament_index(request):
    tournaments = Tournament.tournament.all()
    return render(request, 'GolfApp/tournamentIndex.html', {'tournaments': tournaments})

def tournament_details(request,pk):
    pk = int(pk)
    tournament_details = Tournament.tournament.get(id=pk)
    return render(request, 'GolfApp/tournamentDetails.html', {'tournament_details': tournament_details})

def tournament_delete(request,pk):
    pk = int(pk)
    tournament_deleted = Tournament.tournament.get(id=pk)
    deleted = tournament_deleted.tournament_name
    tournament_deleted.delete()
    return render(request, 'GolfApp/deleteConfirmed.html', {'deleted': deleted})

def player_delete(request,pk):
    pk = int(pk)
    player_deleted = Player.player.get(id=pk)
    deleted = player_deleted.player_name
    player_deleted.delete()
    return render(request, 'GolfApp/deleteConfirmed.html', {'deleted': deleted})

def player_edit(request,pk):
    instance = get_object_or_404(Player, id=pk)
    form = PlayerForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('/Players')
    return render(request, 'GolfApp/playerEdit.html', {'form': form})

def tournament_edit(request, pk):
    instance = get_object_or_404(Tournament, id=pk)
    form = TournamentForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('/Tournaments')
    return render(request, 'GolfApp/tournamentEdit.html', {'form': form})

def golf_news(request):
    news_url = "https://www.pgatour.com/news.html"
    r = requests.get(news_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    divs = soup.find_all('div', attrs={'class': 'inner-text'})
    content = []
    for i in divs:
        article = {}
        article['title'] = i.h4.text
        article['url'] = i.a['href']
        article['img'] = i.img['src']
        article['p'] = i.p.text
        content.append(article)
    return render(request, 'GolfApp/golfAppNews.html', {'content': content})

def player_api(request, year):
    URL = "https://api.sportsdata.io/golf/v2/json/PlayerSeasonStats/" + str(year) + "?key=11cf62dea97c4831b1627a86891b7949"
    r = requests.get(URL)
    content = r.json()
    return render(request, 'GolfApp/golfAppPlayers.html', {'content': content, 'year': year})

def player_api_details(request, id):
    if request.method == "POST":
        favorite = Favorite()
        favorite.player_name = str(request.POST.get('player_name'))
        favorite.picture = str(request.POST.get('picture'))
        favorite.pga_debut = str(request.POST.get('pga_debut'))
        favorite.college = str(request.POST.get('college'))
        favorite.country = str(request.POST.get('country'))
        favorite.born = str(request.POST.get('born'))
        favorite.save()
        return redirect('/Favorites')
    URL = "https://api.sportsdata.io/golf/v2/json/Player/" + str(id) + "?key=11cf62dea97c4831b1627a86891b7949"
    r = requests.get(URL)
    content = r.json()
    return render(request, 'GolfApp/golfAppPlayerDetails.html', {'content': content})

def courses_near_me_api(request):
    if request.method == "POST":
        try:
            zip_code = int(request.POST.get('zip_code'))
            zip_url = "http://api.positionstack.com/v1/forward?access_key=53bb371b4f6110d0cd917a728ad44ab5&query=" + str(zip_code)
            r = requests.get(zip_url)
            c = r.json()['data'][0]
            lat = c['latitude']
            lon = c['longitude']
            weather_url = "http://api.openweathermap.org/data/2.5/forecast?lat=" + str(lat) + "&lon=" + str(lon) + "&appid=e193d5188cdcdb84b811a762d701f520"
            w = requests.get(weather_url)
            w1 = w.json()
            temp = 0
            counter = 0
            for i in w1['list']:
                if counter == 8:
                    break
                kelvin = i['main']['temp']
                kelvin = (int(kelvin) - 273.15) * 9/5 + 32
                if kelvin > temp:
                    temp = kelvin
                counter += 1
            skies = w1['list'][0]['weather'][0]['description']
            approval = {}
            if temp < 55:
                approval['text'] = 'TOO COLD!'
                approval['color'] = 'text-primary'
            elif temp > 90:
                approval['text'] = 'TOO HOT!'
                approval['color'] = 'text-danger'
            else:
                approval['text'] = 'PERFECT FOR GOLF!'
                approval['color'] = 'text-success'
            api_key = '9G_jQANUrQPGT55MtipT-9qKuNqxTUGnB4h-8GUQmTg'
            url = "https://discover.search.hereapi.com/v1/discover?at=" + str(lat) + "," + str(lon) + "&q=Golf+Course&limit=10&lang=en-US&apiKey=" + api_key
            r = requests.get(url)
            contents = r.json()
            return render(request, 'GolfApp/golfCoursesNearMe.html', {'approval':approval,'skies':skies,'contents': contents, 'zip_code':zip_code,'temp': int(temp)})
        except:
            errors = "Please enter a valid ZIP code."
            return render(request, 'GolfApp/golfCoursesNearMe.html', {'contents': None, 'errors': errors})
    return render(request, 'GolfApp/golfCoursesNearMe.html',{'contents': None})

def favorites_index(request):
    content = Favorite.favorite.all()
    return render(request, 'GolfApp/favoritesIndex.html', {'content': content})

def favorite_delete(request, pk):
    pk = int(pk)
    favorite_deleted = Favorite.favorite.get(id=pk)
    deleted = favorite_deleted.player_name
    favorite_deleted.delete()
    return render(request, 'GolfApp/deleteConfirmed.html', {'deleted': deleted})

    # Create your views here.
