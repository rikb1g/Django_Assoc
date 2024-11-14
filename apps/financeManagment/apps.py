from django.apps import AppConfig


class FinancemanagmentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.financeManagment"

    def ready(self) -> None:
        import apps.financeManagment.signals