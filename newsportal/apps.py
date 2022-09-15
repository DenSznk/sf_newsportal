from django.apps import AppConfig


class NewsportalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsportal'


class PostConfig(AppConfig):
    name = 'newsportal'

    def ready(self):
        import newsportal.signals