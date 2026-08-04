import factory
from factory.django import DjangoModelFactory
from tags.models import Tag


class TagFactory(DjangoModelFactory):
    name = factory.Faker("word")

    class Meta:
        model = Tag
