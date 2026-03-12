from django.apps import AppConfig


class HealthCareAppConfig(AppConfig):
    # default_auto_field = 'django.db.models.BigAutoField'
    name = 'HealthCareapp'
    def ready(self):
        import HealthCareapp