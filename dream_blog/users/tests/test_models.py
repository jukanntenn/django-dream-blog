from unittest.mock import MagicMock

import pytest

from dream_blog.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestUser:
    def test_social_avatar_url_with_prefetched_socialaccounts(self):
        user = UserFactory()
        mock_socialaccount = MagicMock()
        mock_socialaccount.get_avatar_url.return_value = "http://example.com/avatar.jpg"
        user.socialaccounts = [mock_socialaccount]

        assert user.social_avatar_url() == "http://example.com/avatar.jpg"

    def test_social_avatar_url_without_prefetched(self):
        user = UserFactory()
        # No socialaccounts attribute, falls back to socialaccount_set
        assert user.social_avatar_url() == ""

    def test_social_avatar_url_with_empty_socialaccounts(self):
        user = UserFactory()
        user.socialaccounts = []
        assert user.social_avatar_url() == ""
