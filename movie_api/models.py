from django.db import models

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Director(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Actor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Movie(models.Model):
    title = models.CharField(max_length=200)
    release_date = models.DateField()
    imbd_rating = models.DecimalField(max_digits=20, decimal_places=10)
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre)
    actors = models.ManyToManyField(Actor)

    def __str__(self):
        return self.title
    