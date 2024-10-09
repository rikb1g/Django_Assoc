from django.apps import AppConfig


class StudentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.student"

    def ready(self):
        import apps.student.signals

