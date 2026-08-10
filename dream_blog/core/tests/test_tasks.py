from unittest.mock import MagicMock, patch

import pytest


@pytest.mark.django_db
class TestBackupDb:
    @patch("django.core.management.call_command")
    def test_calls_dbbackup(self, mock_call_command):
        from dream_blog.core.tasks import backup_db

        backup_db.func()
        mock_call_command.assert_called_once_with("dbbackup", "--clean")


@pytest.mark.django_db
class TestPingHcEmailServiceCheck:
    def test_sends_email_when_ping_email_set(self):
        from dream_blog.core import tasks
        from dream_blog.core.tasks import ping_hc_email_service_check

        original_settings = tasks.settings
        try:
            mock_settings = MagicMock()
            mock_settings.HC_EMAIL_SERVICE_PING_EMAIL = "ping@example.com"
            mock_settings.DEFAULT_FROM_EMAIL = "from@example.com"
            tasks.settings = mock_settings

            with patch("dream_blog.core.tasks.send_mail") as mock_send_mail:
                ping_hc_email_service_check.func()
                mock_send_mail.assert_called_once()
        finally:
            tasks.settings = original_settings

    def test_does_nothing_when_no_ping_email(self):
        from dream_blog.core import tasks
        from dream_blog.core.tasks import ping_hc_email_service_check

        original_settings = tasks.settings
        try:
            mock_settings = MagicMock()
            mock_settings.HC_EMAIL_SERVICE_PING_EMAIL = None
            tasks.settings = mock_settings

            with patch("dream_blog.core.tasks.send_mail") as mock_send_mail:
                ping_hc_email_service_check.func()
                mock_send_mail.assert_not_called()
        finally:
            tasks.settings = original_settings
