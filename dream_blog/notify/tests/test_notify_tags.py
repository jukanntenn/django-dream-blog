from unittest.mock import MagicMock, patch

import pytest
from notify.templatetags.notify_tags import display, frag

from dream_blog.notify.factories import NotificationFactory

pytestmark = pytest.mark.django_db


class TestFrag:
    def test_returns_template_for_comment_verb(self):
        notification = NotificationFactory(verb="comment")
        assert frag(notification) == "notifications/comment.html"

    def test_returns_template_for_reply_verb(self):
        notification = NotificationFactory(verb="reply")
        assert frag(notification) == "notifications/reply.html"


class TestDisplay:
    def test_returns_empty_for_unknown_verb(self):
        notification = NotificationFactory(verb="unknown_verb")
        result = display(notification)
        assert result == ""

    @patch("notify.templatetags.notify_tags.render_to_string")
    @patch("notify.templatetags.notify_tags.settings")
    def test_returns_rendered_template_for_known_verb(self, mock_settings, mock_render):
        mock_settings.NOTIFICATION_TEMPLATES = {"comment": "notifications/comment.html"}
        mock_render.return_value = "<p>rendered</p>"

        notification = NotificationFactory(verb="comment")
        result = display(notification)
        assert result == "<p>rendered</p>"
        mock_render.assert_called_once()

    @patch("notify.templatetags.notify_tags.render_to_string")
    @patch("notify.templatetags.notify_tags.settings")
    def test_passes_request_to_context(self, mock_settings, mock_render):
        mock_settings.NOTIFICATION_TEMPLATES = {"comment": "notifications/comment.html"}
        mock_render.return_value = "<p>rendered</p>"

        notification = NotificationFactory(verb="comment")
        request = MagicMock()
        display(notification, request=request)

        call_kwargs = mock_render.call_args
        assert call_kwargs[1]["context"]["request"] == request
