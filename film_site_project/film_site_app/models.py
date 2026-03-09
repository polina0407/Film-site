from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class Genre(models.Model):
    genre = models.CharField(max_length=255)

    def __str__(self):
        return self.genre


class Film(models.Model):
    title = models.CharField(max_length=255)
    production_date = models.DateField()
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="films")
    country = models.CharField(max_length=255)
    trailer_url = models.URLField(blank=True)

    def __str__(self):
        return self.title


class Actor(models.Model):
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    gender_choices = [
        ("male", "Чоловік"),
        ("female", "Жінка"),
        ("no_info", "Не бажаю вказувати"),
    ]
    gender = models.CharField(max_length=20, choices=gender_choices)

    country = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="actor_photos/")

    def __str__(self):
        return f"{self.name} {self.last_name}"


class Role(models.Model):
    title = models.CharField(max_length=255)
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name="roles")
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name="roles")

    def __str__(self):
        return f"{self.actor} - {self.title} ({self.film})"


class Profile(AbstractUser):

    ROLES = [('admin', 'Адміністратор'), ('client', 'Клієнт')]

    gender_choices = [("male", "Чоловік"), ("female", "Жінка"), ("no info", "Не бажаю вказувати ")]

    gender = models.CharField(max_length=20, choices=gender_choices)
    avatar = models.ImageField(upload_to='pofile_avatars/', blank=True)
    liked_film = models.ManyToManyField(Film, blank=True, related_name="liked_by")
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.username
