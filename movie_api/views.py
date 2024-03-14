from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from .models import Movie, Actor, Director, Genre
from .serializers import MovieSerializer, ActorSerializer, DirectorSerializer, GenreSerializer
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime


# Create your views here.

def user_in_specific_group(user):
    return user.is_authenticated and user.groups.filter(name='Admin').exists()


def home(request):
    return JsonResponse({"success":"Welcome to Movie API"}, status=201)


def getMovies(request):
    allMovies = Movie.objects.all()
    serializer = MovieSerializer(allMovies, many=True)
    return JsonResponse(serializer.data, safe=False)


def getActors(request):
    allActors = Actor.objects.all()
    serializer = ActorSerializer(allActors, many=True)
    return JsonResponse(serializer.data, safe=False)    


def getDirectors(request):
    allDirectors = Director.objects.all()
    serializer = DirectorSerializer(allDirectors, many=True)
    return JsonResponse(serializer.data, safe=False)  


def getGenre(request):
    allGenre = Genre.objects.all()
    serializer = GenreSerializer(allGenre, many=True)
    return JsonResponse(serializer.data, safe=False)  


def movieItem(request, id):
    movie = Movie.objects.filter(id=id).first()
    if movie is not None:
        serializer = MovieSerializer(movie)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({"error":f"Movie Not Found with id='{id}'"}, status=400)  


def directorItem(request, id):
    director = Director.objects.filter(id=id).first()
    if director is not None:
        serializer = DirectorSerializer(director)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({"error":f"Director Not Found with id='{id}'"}, status=400)    



def actorItem(request, id):
    actor = Actor.objects.filter(id=id).first()
    if actor is not None:
        serializer = ActorSerializer(actor)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({"error":f"Actor Not Found with id='{id}'"}, status=400)


def genreItem(request, id):
    genre = Genre.objects.filter(id=id).first()
    if genre is not None:
        serializer = GenreSerializer(genre)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({"error":f"Genre Not Found with id='{id}'"}, status=400)    
   


def filterByGenre(request, id):
    movies = Movie.objects.filter(genres__id=id)
    serializer = MovieSerializer(movies, many=True)
    return JsonResponse(serializer.data, safe=False)


def filterByDirector(request, id):
    movies = Movie.objects.filter(director__id=id)
    serializer = MovieSerializer(movies, many=True)
    return JsonResponse(serializer.data, safe=False)    


def filterByActor(request, id):
    movies = Movie.objects.filter(actors__id=id)
    serializer = MovieSerializer(movies, many=True)
    return JsonResponse(serializer.data, safe=False)     


def getMoviesUnderRating(request, num):
    movies = Movie.objects.filter(imbd_rating__lt=num)
    serializer = MovieSerializer(movies, many=True)
    return JsonResponse(serializer.data, safe=False)


def getMoviesAboveRating(request, num):
    movies = Movie.objects.filter(imbd_rating__gt=num)
    serializer = MovieSerializer(movies, many=True)
    return JsonResponse(serializer.data, safe=False)    


def getMoviesEqualRating(request, num):
    movies = Movie.objects.filter(imbd_rating = num)
    if movies.exists():
        serializer = MovieSerializer(movies, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({"error":f"No movie found with rating='{num}"}, status=400)    


def getMoviesByYear(request, year):
    movies = Movie.objects.filter(release_date__year = year)
    if movies.exists():
        serializer = MovieSerializer(movies, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({"error":f"No movie found with year='{year}'"}, status=404)    


@csrf_exempt
def createUser(request):
    if request.method == 'POST':
        if 'username' in request.POST and 'password' in request.POST and 'group' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            group = request.POST['group']

            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists. Please enter a unique username."}, status=400)   

            try:
                group = Group.objects.get(name=group)
            except Group.DoesNotExist:
                return JsonResponse({"error": f"Group '{group}' does not exist."}, status=400)

            user = User.objects.create_user(username=username, password=password)
            user.groups.add(group)

            return JsonResponse({"success": "User created successfully."}, status=201)   
        else:
            return JsonResponse({"error": "Username, password, and group are required."}, status=400)
    else:
        return JsonResponse({"error": "Method not allowed."}, status=405)


@csrf_exempt
def handleLogin(request):
    if request.method == "POST":
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(request, username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            return JsonResponse({"success":"User logged in sccessfully"}, status=201)
        else:
            return JsonResponse({"error":"Invalid Credentials, try again."}, status=400)
    else:
        return JsonResponse({"error": "Method not allowed."}, status=405)


def handleLogout(request):
    logout(request)
    return JsonResponse({"success":"User Logged Out Successfully"}, status=201) 


@user_passes_test(user_in_specific_group)
@csrf_exempt
def add_actor(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if not name:
            return JsonResponse({'error': 'Actor name is required'}, status=400)
        if Actor.objects.filter(name=name).exists():
            return JsonResponse({'error': 'Actor with this name already exists'}, status=400)
        else:
            actor = Actor(name=name)
            actor.save()
            return JsonResponse({'success': 'Actor added successfully'}, status=201)
    else:
        return JsonResponse({"error": "Method not allowed."}, status=405)


@user_passes_test(user_in_specific_group)
@csrf_exempt
def add_director(request):
    if request.method=='POST':
        name = request.POST.get('name')
        if not name:
            return JsonResponse({'error': 'Director name is required'}, status=400)
        if Director.objects.filter(name=name).exists():
            return JsonResponse({"error":"Director with this name already exists"}, status=400)
        else:
            director = Director(name=name)
            director.save()
            return JsonResponse({'success':"Director added successfully"}, status=201)
    else:
        return JsonResponse({"error": "Method not allowed."}, status=405)


@user_passes_test(user_in_specific_group)
@csrf_exempt
def add_genre(request):
    if request.method=='POST':
        name=request.POST.get('name')
        if not name:
            return JsonResponse({'error': 'Genre name is required'}, status=400)
        if Genre.objects.filter(name=name).exists():
            return JsonResponse({"error":"Genre with this name already exists"}, status=400)
        else:
            genre = Genre(name=name)
            genre.save()
            return JsonResponse({'success':"Genre added successfully"}, status=201)
    else:
        return JsonResponse({"error": "Method not allowed."}, status=405)           


@user_passes_test(user_in_specific_group)
@csrf_exempt
def add_movie(request):
    if request.method == 'POST':
        # Extract movie data from the request
        title = request.POST.get('title')
        release_date = request.POST.get('release_date')
        imbd_rating = request.POST.get('imbd_rating')
        director_name = request.POST.get('director')
        genres_str = request.POST.get('genres')
        actors_str = request.POST.get('actors')

        if not all([title, release_date, imbd_rating, director_name, genres_str, actors_str]):
            return JsonResponse({'error': 'Please fill all fields'}, status=400)

        try:
            release_date = datetime.strptime(release_date, '%Y-%m-%d').date()
            imbd_rating = float(imbd_rating)
        except ValueError:
            return JsonResponse({'error': 'Invalid release date or IMBD rating format'}, status=400)

        director = Director.objects.filter(name=director_name).first()
        if not director:
            return JsonResponse({'error': 'Director does not exist'}, status=400)

        genre_names = genres_str.split(',')
        actor_names = actors_str.split(',')

        genres = []
        for genre_name in genre_names:
            genre, _ = Genre.objects.get_or_create(name=genre_name.strip())
            genres.append(genre)

        actors = []
        for actor_name in actor_names:
            actor, _ = Actor.objects.get_or_create(name=actor_name.strip())
            actors.append(actor)

        if Movie.objects.filter(title=title).exists():
            return JsonResponse({'error': 'Duplicate movie already exists'}, status=400)

        else:
            movie = Movie.objects.create(
            title=title,
            release_date=release_date,
            imbd_rating=imbd_rating,
            director=director
            )
            movie.genres.add(*genres)
            movie.actors.add(*actors)

            movie.save()

            return JsonResponse({'success': 'Movie added successfully'}, status=201)

        
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@user_passes_test(user_in_specific_group)
@csrf_exempt
def delete_actor(request, id):
    if request.method == 'DELETE':
        actor = Actor.objects.filter(id=id).first()
        if actor is not None:
            actor.delete()
            return JsonResponse({'success': 'Actor deleted successfully'}, status=201)
        else:
            return JsonResponse({"error":f"Actor Not Found with id='{id}'"}, status=400)  
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)              


@user_passes_test(user_in_specific_group)
@csrf_exempt
def delete_director(request, id):
    if request.method == 'DELETE':
        director = Director.objects.filter(id=id).first()
        if director is not None:
            director.delete()
            return JsonResponse({'success': 'Director deleted successfully'}, status=201)
        else:
            return JsonResponse({"error":f"Director Not Found with id='{id}'"}, status=400) 
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)        


@user_passes_test(user_in_specific_group)
@csrf_exempt
def delete_genre(request, id):
    if request.method == 'DELETE':
        genre = Genre.objects.filter(id=id).first()
        if genre is not None:
            genre.delete()
            return JsonResponse({'success': 'Genre deleted successfully'}, status=201)
        else:
            return JsonResponse({"error":f"Genre Not Found with id='{id}'"}, status=400)   
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)              


@user_passes_test(user_in_specific_group)
@csrf_exempt
def delete_movie_id(request, id):
    if request.method == 'DELETE':
        movie = Movie.objects.filter(id=id).first()
        if movie is not None:
            movie.delete()
            return JsonResponse({'success': 'Movie deleted successfully'}, status=201)
        else:
            return JsonResponse({"error":f"Movie Not Found with id='{id}'"}, status=400) 
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@user_passes_test(user_in_specific_group)
@csrf_exempt
def delete_movie_name(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if not title:
            return JsonResponse({'error': 'Movie name is required'}, status=400)
        if Movie.objects.filter(title=title).exists():
            movie = Movie.objects.filter(title=title)
            movie.delete() 
            return JsonResponse({'success': f'Movie "{title}" deleted successfully'}, status=200)
        else:
            return JsonResponse({"error": f'Movie with name "{title}" does not exist'}, status=404)
    else:
        return JsonResponse({"error": "Method not allowed."}, status=405)
