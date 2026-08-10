import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from dream_blog.posts.models import Post
from dream_blog.users.tests.factories import UserFactory


class PostFactory(DjangoModelFactory):
    title = factory.Faker("sentence")
    content = factory.Faker("paragraph")
    excerpt = factory.Faker("sentence")
    publish_date = factory.LazyFunction(timezone.now)

    author = factory.SubFactory(UserFactory)

    class Meta:
        model = Post
