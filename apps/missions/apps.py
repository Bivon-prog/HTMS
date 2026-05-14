from django.apps import AppConfig


class MissionsConfig(AppConfig):
    default_auto_field = 'django_mongodb_backend.fields.ObjectIdAutoField'
    name = 'apps.missions'
    label = 'missions'
