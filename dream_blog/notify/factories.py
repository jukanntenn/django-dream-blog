import factory
from factory.django import DjangoModelFactory
from notifications.models import Notification

from dream_blog.users.tests.factories import UserFactory


class NotificationFactory(DjangoModelFactory):
    class Meta:
        model = Notification

    recipient = factory.SubFactory(
        UserFactory, username=factory.Sequence(lambda n: f"recipient_{n}")
    )
    actor = factory.SubFactory(UserFactory, username=factory.Sequence(lambda n: f"actor_{n}"))
    verb = "comment"
