# Django imports
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.statistics"

    def ready(self) -> None:
        # return super().ready()
        import apps.statistics.signals
