from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FriendlinksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dream_blog.friendlinks"
    verbose_name = _("Friend Links")
