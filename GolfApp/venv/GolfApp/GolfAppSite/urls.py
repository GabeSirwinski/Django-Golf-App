from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='GolfHome'),
    path('CreatePlayer/', views.create_new_player, name="create_player"),
    path('Players/', views.index, name="player_index"),
    path('Players/<int:pk>/Details', views.details, name="player_details"),
    path('CreateTournament/', views.create_new_tournament, name="create_tournament"),
    path('Tournaments/', views.tournament_index, name="tournament_index"),
    path('Tournaments/<int:pk>/Details', views.tournament_details, name="tournament_details"),
    path('<int:pk>/Tournament/deleteConfirmed', views.tournament_delete, name="tournament_delete"),
    path('<int:pk>/Player/deleteConfirmed', views.player_delete, name="player_delete"),
    path('<int:pk>/Player/Edit', views.player_edit, name="player_edit"),
    path('<int:pk>/Tournament/Edit', views.tournament_edit, name="tournament_edit"),
    path('News/', views.golf_news, name="golf_news"),
    path('pgaPlayers/<int:year>', views.player_api, name="player_api"),
    path('pgaPlayers/Player/<int:id>', views.player_api_details, name="player_api_details"),
    path('coursesNearMe/', views.courses_near_me_api, name="courses_near_me_api"),
    path('Favorites/', views.favorites_index, name='favorites_index'),
    path('Favorites/<int:pk>/deleteConfirmed', views.favorite_delete, name='favorite_delete'),


]