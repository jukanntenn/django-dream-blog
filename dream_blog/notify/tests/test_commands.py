import pytest
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from notifications.models import Notification
from users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestFixStaleNotifications:
    def test_handles_no_old_content_type(self, capsys):
        """When no stale ContentType exists, prints warning."""
        call_command("fix_stale_notifications")
        captured = capsys.readouterr()
        assert "No stale ContentType found" in captured.out or "Nothing to do" in captured.out

    def test_handles_no_affected_notifications(self, capsys):
        """When old ContentType exists but no notifications use it."""
        ContentType.objects.get_or_create(app_label="tree_comments", model="treecomment")
        call_command("fix_stale_notifications")
        captured = capsys.readouterr()
        assert "No affected notifications found" in captured.out

    def test_updates_stale_notifications(self, capsys):
        """When stale notifications exist, updates them."""
        user = UserFactory()

        old_ct, _ = ContentType.objects.get_or_create(app_label="tree_comments", model="treecomment")
        new_ct = ContentType.objects.get_for_model(Comment)

        # Create a notification with the old ContentType
        Notification.objects.create(
            recipient=user,
            actor=user,
            verb="comment",
            target_content_type=old_ct,
            target_object_id="1",
        )

        call_command("fix_stale_notifications")
        captured = capsys.readouterr()
        assert "Successfully updated" in captured.out

        # Verify the notification was updated
        notif = Notification.objects.first()
        assert notif.target_content_type == new_ct
