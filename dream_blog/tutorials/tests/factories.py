import factory
from django.utils import timezone
from django.utils.text import slugify
from factory.django import DjangoModelFactory
from tutorials.models import Category, Material, Tutorial
from users.tests.factories import UserFactory


class CategoryFactory(DjangoModelFactory):
    name = factory.Faker("name")

    class Meta:
        model = Category


class TutorialFactory(DjangoModelFactory):
    title = factory.Faker("sentence")
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))
    excerpt = factory.Faker("sentence")
    content = factory.Faker("paragraph")
    status = Tutorial.STATUS.completed

    author = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)

    class Meta:
        model = Tutorial


class MaterialFactory(DjangoModelFactory):
    title = factory.Faker("sentence")
    content = factory.Faker("paragraph")
    publish_date = factory.LazyFunction(timezone.now)

    tutorial = factory.SubFactory(TutorialFactory)

    class Meta:
        model = Material
