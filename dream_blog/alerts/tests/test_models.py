import pytest

from alerts.models import Alert
from posts.tests.factories import PostFactory

pytestmark = pytest.mark.django_db


def test_alert_creation_defaults():
    post = PostFactory()
    alert = Alert.objects.create(text="Test alert", content_object=post)

    assert alert.text == "Test alert"
    assert alert.show is True
    assert alert.rank == 0


def test_alert_str_returns_preview():
    post = PostFactory()
    text = "This is a very long alert message that should be truncated"
    alert = Alert.objects.create(text=text, content_object=post)

    assert str(alert) == text[:30]


def test_alert_generic_foreign_key_resolves():
    post = PostFactory()
    alert = Alert.objects.create(text="Post alert", content_object=post)

    assert alert.content_object == post


def test_alert_ordering_by_rank():
    post = PostFactory()
    alert1 = Alert.objects.create(text="First alert", content_object=post, rank=2)
    alert2 = Alert.objects.create(text="Second alert", content_object=post, rank=1)

    assert list(Alert.objects.all()) == [alert2, alert1]
