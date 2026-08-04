import factory
from columns.models import Article, Column
from factory.django import DjangoModelFactory
from users.tests.factories import UserFactory


class ColumnFactory(DjangoModelFactory):
    title = factory.Faker("sentence")
    slug = factory.LazyAttribute(lambda obj: obj.title.lower().replace(" ", "-")[:50])
    excerpt = factory.Faker("paragraph")
    content = factory.Faker("paragraph")
    author = factory.SubFactory(UserFactory)

    class Meta:
        model = Column


class ArticleFactory(DjangoModelFactory):
    title = factory.Faker("sentence")
    content = factory.Faker("paragraph")
    column = factory.SubFactory(ColumnFactory)

    class Meta:
        model = Article
