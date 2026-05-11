from django.contrib import admin
from .models import Genre, Film, Actor, Role, Profile

# Register your models here.
admin.site.register(Genre)
admin.site.register(Film)
admin.site.register(Actor)
admin.site.register(Role)
admin.site.register(Profile)