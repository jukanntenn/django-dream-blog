from unittest.mock import MagicMock, patch

import pytest
from comments.moderation import CommentModerator, Moderator
from posts.models import Post
from posts.tests.factories import PostFactory
from users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestModerator:
    def test_post_save_moderation_unregistered_model(self):
        moderator = Moderator()
        comment = MagicMock()
        comment.content_type.model_class.return_value = str  # not registered
        request = MagicMock()
        # Should not raise
        moderator.post_save_moderation(sender=None, comment=comment, request=request)

    @patch("comments.moderation.notify.send")
    def test_post_save_moderation_registered_model(self, mock_notify):
        moderator = Moderator()
        moderator.register(Post, CommentModerator)

        user = UserFactory()
        post = PostFactory(author=user)

        comment = MagicMock()
        comment.content_type.model_class.return_value = Post
        comment.user = user
        comment.content_object = post
        comment.parent = None
        comment.pk = 1
        request = MagicMock()
        request.build_absolute_uri.return_value = "http://example.com"

        with (
            patch("comments.moderation.loader") as mock_loader,
            patch("comments.moderation.get_current_site") as mock_site,
        ):
            mock_site.return_value = MagicMock()
            mock_template = MagicMock()
            mock_loader.get_template.return_value = mock_template
            mock_template.render.return_value = "rendered"

            moderator.post_save_moderation(sender=None, comment=comment, request=request)

        # Author commenting on own post - no notification
        mock_notify.assert_not_called()


class TestCommentModerator:
    @pytest.fixture
    def moderator(self):
        return CommentModerator(Post)

    @pytest.fixture
    def post(self, user):
        return PostFactory(author=user)

    @patch("comments.moderation.notify.send")
    def test_notify_author_comment_on_own_post(self, mock_notify, moderator, user, post):
        """When author comments on own post, no notification is sent."""
        comment = MagicMock()
        comment.user = user
        comment.parent = None

        moderator.notify(comment, post, MagicMock())
        mock_notify.assert_not_called()

    @patch("comments.moderation.notify.send")
    @patch("comments.moderation.loader")
    @patch("comments.moderation.get_current_site")
    def test_notify_other_user_comments_on_post(self, mock_site, mock_loader, mock_notify, moderator, user, post):
        """When another user comments, author gets notification."""
        other_user = UserFactory()
        comment = MagicMock()
        comment.user = other_user
        comment.parent = None
        comment.pk = 1
        request = MagicMock()
        request.build_absolute_uri.return_value = "http://example.com"

        mock_site.return_value = MagicMock()
        mock_template = MagicMock()
        mock_loader.get_template.return_value = mock_template
        mock_template.render.return_value = "rendered"

        # Mock the recipient email_user
        user.email_user = MagicMock()

        moderator.notify(comment, post, request)

        mock_notify.assert_called_once()
        call_kwargs = mock_notify.call_args
        assert call_kwargs[1]["recipient"] == user
        assert call_kwargs[1]["verb"] == "comment"

    @patch("comments.moderation.notify.send")
    @patch("comments.moderation.loader")
    @patch("comments.moderation.get_current_site")
    def test_notify_reply_to_another_user(self, mock_site, mock_loader, mock_notify, moderator, user, post):
        """When user replies to another user, both get notifications."""
        replier = UserFactory()
        parent_user = UserFactory()
        parent_comment = MagicMock()
        parent_comment.user = parent_user

        comment = MagicMock()
        comment.user = replier
        comment.parent = parent_comment
        comment.pk = 1
        request = MagicMock()
        request.build_absolute_uri.return_value = "http://example.com"

        mock_site.return_value = MagicMock()
        mock_template = MagicMock()
        mock_loader.get_template.return_value = mock_template
        mock_template.render.return_value = "rendered"

        parent_user.email_user = MagicMock()

        moderator.notify(comment, post, request)

        assert mock_notify.call_count == 2

    @patch("comments.moderation.notify.send")
    @patch("comments.moderation.loader")
    @patch("comments.moderation.get_current_site")
    def test_notify_reply_to_self(self, mock_site, mock_loader, mock_notify, moderator, user, post):
        """When user replies to themselves, no notification is sent."""
        comment = MagicMock()
        comment.user = user
        parent_comment = MagicMock()
        parent_comment.user = user
        comment.parent = parent_comment
        comment.pk = 1
        request = MagicMock()
        request.build_absolute_uri.return_value = "http://example.com"

        mock_site.return_value = MagicMock()
        mock_template = MagicMock()
        mock_loader.get_template.return_value = mock_template
        mock_template.render.return_value = "rendered"

        moderator.notify(comment, post, request)
        mock_notify.assert_not_called()

    @patch("comments.moderation.send_mail")
    @patch("comments.moderation.loader")
    @patch("comments.moderation.get_current_site")
    def test_email_sends_to_managers(self, mock_site, mock_loader, mock_send_mail, moderator, user, post):
        """email() sends notification to MANAGERS."""
        comment = MagicMock()
        comment.pk = 1
        request = MagicMock()
        request.build_absolute_uri.return_value = "http://example.com"

        mock_site.return_value = MagicMock()
        mock_template = MagicMock()
        mock_loader.get_template.return_value = mock_template
        mock_template.render.return_value = "rendered"

        with pytest.MonkeyPatch.context() as m:
            m.setattr("django.conf.settings.MANAGERS", [("Admin", "admin@example.com")])
            m.setattr("django.conf.settings.DEFAULT_FROM_EMAIL", "from@example.com")
            moderator.email(comment, post, request)

        mock_send_mail.assert_called_once()

    def test_email_disabled(self, moderator, user, post):
        """email() does nothing when email_notification is False."""
        moderator.email_notification = False
        comment = MagicMock()
        request = MagicMock()
        # Should not raise
        moderator.email(comment, post, request)
