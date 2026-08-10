from typing import TYPE_CHECKING

from django.contrib.auth.models import AbstractUser
from django.db import models

if TYPE_CHECKING:
    from allauth.socialaccount.models import SocialAccount
    from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    # Reverse relations from django-allauth; declared for static analysis.
    socialaccounts: "list[SocialAccount]"
    socialaccount_set: "QuerySet[SocialAccount]"

    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]

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
