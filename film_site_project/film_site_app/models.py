from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.

class Genre(models.Model):

    genre = models.CharField(max_length=255)
    def __str__(self):
        return self.genre


class Film(models.Model)




class Profile(AbstractUser):

    phone = models.CharField(max_length=20, blank=True)
    gender_choices = [ ("male", "Чоловік"),("female", "Жінка"),("no info", "Не бажаю вказувати ") ]
    gender = models.CharField(max_length=20, choices=gender_choices,)
    avatar = models.ImageField(upload_to='pofile_avatars/')
    liked_film = models.ManyToManyField(Film)

    def __str__(self):
        return self.username


