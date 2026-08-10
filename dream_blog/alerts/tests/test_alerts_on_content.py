import pytest
from django.utils.text import slugify

from dream_blog.alerts.models import Alert
from dream_blog.columns.models import Article, Column
from dream_blog.core.models import AlertsModel

pytestmark = pytest.mark.django_db


def test_alerts_model_is_abstract():
    assert AlertsModel._meta.abstract is True


def test_alerts_on_post(post):
    Alert.objects.create(text="Post alert", content_object=post)
    assert post.alerts.count() == 1


def test_alerts_on_material(material):
    Alert.objects.create(text="Material alert", content_object=material)
    assert material.alerts.count() == 1


def test_alerts_on_article(user):
    column = Column.objects.create(
        title="Test Column",
        slug=slugify("Test Column"),
        excerpt="excerpt",
        content="content",
        author=user,
    )
    article = Article.objects.create(
        column=column,
        title="Test Article",
        content="content",
    )
    Alert.objects.create(text="Article alert", content_object=article)
    assert article.alerts.count() == 1


def test_alert_ranking_order_on_relation(post):
    Alert.objects.create(text="Third", content_object=post, rank=3)
    Alert.objects.create(text="First", content_object=post, rank=1)
    Alert.objects.create(text="Second", content_object=post, rank=2)

    assert [a.text for a in post.alerts.all()] == ["First", "Second", "Third"]
