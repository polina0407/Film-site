from django.apps import AppConfig


class FilmSiteAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'film_site_app'

    def ready(self):
        import film_site_app.signals  # Обов'язково імпортуємо сигнали тут
