from django.urls import path, include
from .views import *

urlpatterns = [
    path("", HomeView.as_view(), name="home"),

    path("films/", FilmListView.as_view(), name="film_list"),
    path("films/<int:id>/", FilmDetailView.as_view(), name="film_detail"),

    path("actors/", ActorListView.as_view(), name="actor_list"),
    path("actors/<int:id>/", ActorDetailView.as_view(), name="actor_detail"),

    path("profile/", ProfileView.as_view(), name="profile"),

    path("films/<int:id>/like/", LikeFilmView.as_view(), name="like_film"),
]