from django.apps import AppConfig


class PetBaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.pet_base'
    verbose_name = "база данных питомцев"
