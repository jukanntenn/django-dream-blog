from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WebtoolsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "webtools"
    verbose_name = _("Web Tools")
