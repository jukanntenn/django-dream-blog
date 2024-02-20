from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    name = models.CharField(_("Name of User"), blank=True, max_length=255)

    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def social_avatar_url(self):
        try:
            socialaccount = self.socialaccounts[0]
        except AttributeError:
            socialaccount = self.socialaccount_set.first()
        except IndexError:
            return ""

        if socialaccount is None:
            return ""

        return socialaccount.get_avatar_url()
