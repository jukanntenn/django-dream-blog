import pytest
from notifications.models import Notification

from dream_blog.notify.factories import NotificationFactory
from dream_blog.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_notification_factory_creates_notification():
    notification = NotificationFactory()
    assert isinstance(notification, Notification)
    assert notification.recipient is not None
    assert notification.actor is not None
    assert notification.verb == "comment"


def test_notification_factory_accepts_custom_verb():
    notification = NotificationFactory(verb="reply")
    assert notification.verb == "reply"


def test_notification_factory_creates_unique_users_by_default():
    notification = NotificationFactory()
    assert notification.recipient != notification.actor


def test_notification_factory_allows_same_user_for_actor_and_recipient():
    user = UserFactory()
    notification = NotificationFactory(recipient=user, actor=user)
    assert notification.recipient == notification.actor
