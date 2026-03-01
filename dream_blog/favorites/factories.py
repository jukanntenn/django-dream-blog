import factory
from django.utils import timezone
from factory import django as factory_django

from dream_blog.favorites.models import Favorite, Issue
from dream_blog.users.tests.factories import UserFactory


class IssueFactory(factory_django.DjangoModelFactory):
    class Meta:
        model = Issue

    number = factory.Sequence(lambda n: n + 1)
    pub_date = factory.LazyFunction(timezone.now)
    description = factory.Faker("text", max_nb_chars=200)
    creator = factory.SubFactory(UserFactory)


class FavoriteFactory(factory_django.DjangoModelFactory):
    class Meta:
        model = Favorite

    issue = factory.SubFactory(IssueFactory)
    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("text", max_nb_chars=200)
    url = factory.Faker("url")
    rank = factory.Sequence(lambda n: n)
