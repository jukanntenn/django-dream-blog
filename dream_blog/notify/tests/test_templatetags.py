import pytest

from dream_blog.notify.factories import NotificationFactory
from dream_blog.notify.templatetags.notify_tags import frag

pytestmark = pytest.mark.django_db


def test_frag_filter_comment():
    notification = NotificationFactory(verb="comment")
    assert frag(notification) == "notifications/comment.html"


def test_frag_filter_reply():
    notification = NotificationFactory(verb="reply")
    assert frag(notification) == "notifications/reply.html"


def test_frag_filter_unknown_verb():
    notification = NotificationFactory(verb="unknown")
    assert frag(notification) == "notifications/unknown.html"
