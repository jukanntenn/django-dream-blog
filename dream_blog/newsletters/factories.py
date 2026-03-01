import factory
from factory import Faker
from factory import django as factory_django

from dream_blog.newsletters.models import Subscription
from dream_blog.users.tests.factories import UserFactory


class SubscriptionFactory(factory_django.DjangoModelFactory):
    class Meta:
        model = Subscription

    email = Faker("email")
    user = factory.SubFactory(UserFactory)
    confirmed = False
    active = False
