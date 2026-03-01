import logging
from typing import Optional

from constance import config
from django.apps import apps
from django.core import signing
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)


class EmailConfirmation:
    salt = "django_dream_blog"

    def __init__(self, instance):
        self.instance = instance

    def make_key(self) -> str:
        model_cls = self.instance.__class__
        return signing.dumps(
            obj={
                "app_label": model_cls._meta.app_label,
                "model_name": model_cls._meta.model_name,
                "pk": self.instance.pk,
            },
            salt=self.salt,
        )

    @classmethod
    def from_key(cls, key: str) -> Optional["EmailConfirmation"]:
        try:
            max_age = 60 * 60 * 24 * int(config.EMAIL_CONFIRMATION_EXPIRE_DAYS)
            data = signing.loads(key, max_age=max_age, salt=cls.salt)
            model_cls = apps.get_model(data["app_label"], data["model_name"])
            instance = model_cls._default_manager.get(pk=data["pk"])
            return cls(instance=instance)
        except (
            signing.SignatureExpired,
            signing.BadSignature,
            ObjectDoesNotExist,
            LookupError,
            KeyError,
            TypeError,
            ValueError,
        ) as exc:
            logger.info("Invalid email confirmation key (%s).", exc.__class__.__name__)
            return None
