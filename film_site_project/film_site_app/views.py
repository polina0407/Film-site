from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, DetailView, CreateView, View, TemplateView
from .models import Film, Actor, Genre, Role
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class HomeView(ListView):
    model = Film
    template_name = "other/home.html"
    context_object_name = "films"

    def get_queryset(self):
        return Film.objects.order_by('?')[:10]


class FilmListView(ListView):
    model = Film
    template_name = "films/film_list.html"
    context_object_name = "films"

    def get_queryset(self):
        return Film.objects.select_related("genre").all()


class FilmDetailView(DetailView):
    model = Film
    template_name = "films/film_detail.html"
    context_object_name = "film"
    pk_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["roles"] = Role.objects.filter(
            film=self.object
        ).select_related("actor")

        return context


class ActorListView(ListView):
    model = Actor
    template_name = "actors/actor_list.html"
    context_object_name = "actors"


class ActorDetailView(DetailView):
    model = Actor
    template_name = "actors/actor_detail.html"
    context_object_name = "actor"
    pk_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["roles"] = Role.objects.filter(
            actor=self.object
        ).select_related("film")

        return context


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "other/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        context["profile"] = user
        context["liked_films"] = user.liked_film.all()
        # todo: шо з liked_film чи liked_filmс
        return context


class LikeFilmView(LoginRequiredMixin, View):

    def post(self, request, id):
        film = get_object_or_404(Film, id=id)

        if film in request.user.liked_films.all():
            request.user.liked_films.remove(film)
        else:
            request.user.liked_films.add(film)

        return redirect("film_detail", id=id)



class CustomLoginView(LoginView):
    template_name = "tasks/login.html"
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = "tasks:login"


class RegisterView(CreateView):
    template_name = "tasks/register.html"
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(reverse_lazy("tasks:login"))
