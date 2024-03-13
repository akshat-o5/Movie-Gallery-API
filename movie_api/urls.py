"""
URL configuration for movies project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('getMovies', views.getMovies, name='getMovies'),
    path('getActors', views.getActors, name='getActors'),
    path('getDirectors', views.getDirectors, name='getDirectors'),
    path('getGenre', views.getGenre, name='getGenre'),
    path('movies/<int:id>', views.movieItem, name='movieItem'),
    path('directors/<int:id>', views.directorItem, name='directorItem'),
    path('actors/<int:id>', views.actorItem, name='actorItem'),
    path('genres/<int:id>', views.genreItem, name='genreItem'),
    path('movies/genre/<int:id>', views.filterByGenre, name='filterByGenre'),
    path('movies/director/<int:id>', views.filterByDirector, name='filterByDirector'),
    path('movies/actor/<int:id>', views.filterByActor, name='filterByActor'),
    path('movies/under_imdb_rating/<int:num>', views.getMoviesUnderRating, name='getMoviesUnderRating'),
    path('movies/above_imdb_rating/<int:num>', views.getMoviesAboveRating, name='getMoviesAboveRating'),
    path('movies/equal_imdb_rating/<int:num>', views.getMoviesEqualRating, name='getMoviesEqualRating'),
    path('movies/release_year/<int:year>', views.getMoviesByYear, name='getMoviesByYear'),

    path('create_user', views.createUser, name='createUser'),
    path('handleLogin', views.handleLogin, name='handleLogin'),
    path('handleLogout', views.handleLogout, name='handleLogout'),
    path('add_actor', views.add_actor, name='add_actor'),
    path('add_director', views.add_director, name='add_director'),
    path('add_genre', views.add_genre, name='add_genre'),
    path('add_movie', views.add_movie, name='add_movie'),
]
