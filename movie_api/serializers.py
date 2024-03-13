from rest_framework import serializers
from .models import Genre, Actor, Director, Movie


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'       


class MovieSerializer(serializers.ModelSerializer):
    director = DirectorSerializer()
    genres = GenreSerializer(many=True)
    actors = ActorSerializer(many=True)
    class Meta:
        model = Movie
        fields = '__all__'       