from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, DetailView, CreateView, View, TemplateView
from .models import Film, Actor, Role, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm


class HomeView(ListView):
    model = Film
    template_name = "other/home.html"
    context_object_name = "films"

    def get_queryset(self):
        return Film.objects.order_by('?')[:5]


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
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Передаємо саме об'єкт профілю
        context["profile"] = user.profile
        # Отримуємо фільми через профіль.
        # Назва поля має бути такою ж, як у models.py (у вас там liked_film)
        context["liked_films"] = user.profile.liked_film.all()

        return context


class ProfileEditView(LoginRequiredMixin, View):
    template_name = "accounts/edit_profile.html"

    def get_forms(self, post_data=None, files_data=None):
        """Метод для зручної ініціалізації всіх форм"""
        user = self.request.user
        return {
            'u_form': UserUpdateForm(post_data, instance=user),
            'p_form': ProfileUpdateForm(post_data, files_data, instance=user.profile),
            'pass_form': PasswordChangeForm(user, post_data)
        }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_forms())

    def post(self, request, *args, **kwargs):
        forms = self.get_forms(request.POST, request.FILES)

        # Перевіряємо, яка кнопка була натиснута
        if 'update_profile' in request.POST:
            if forms['u_form'].is_valid() and forms['p_form'].is_valid():
                forms['u_form'].save()
                forms['p_form'].save()
                messages.success(request, "Дані профілю оновлено!")
                return redirect("film_site_app:profile")

        elif 'change_password' in request.POST:
            if forms['pass_form'].is_valid():
                user = forms['pass_form'].save()
                # Важливо, щоб користувач не "вилетів" з системи після зміни пароля
                update_session_auth_hash(request, user)
                messages.success(request, "Пароль успішно змінено!")
                return redirect("film_site_app:profile")

        # Якщо були помилки у валідації, повертаємо форми з помилками
        return render(request, self.template_name, forms)


class LikeFilmView(LoginRequiredMixin, View):
    def post(self, request, id):
        film = get_object_or_404(Film, id=id)

        # Отримуємо профіль поточного користувача
        user_profile = request.user.profile

        # Перевіряємо наявність фільму в списку улюблених профілю
        if film in user_profile.liked_film.all():
            user_profile.liked_film.remove(film)
        else:
            user_profile.liked_film.add(film)

        return redirect("film_site_app:film_detail", id=id)



class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = "film_site_app:login"


class RegisterView(CreateView):
    template_name = "accounts/register.html"
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save()  # Створюємо користувача

        # Створюємо порожній профіль для цього користувача
        #Profile.objects.create(user=user)

        login(self.request, user)
        # Краще редиректити на home або profile, бо користувач вже залогінився
        return redirect("film_site_app:home")
