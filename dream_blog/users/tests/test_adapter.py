from unittest.mock import MagicMock

import pytest
from users.adapter import SocialAccountAdapter
from users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestSocialAccountAdapter:
    @pytest.fixture
    def adapter(self):
        return SocialAccountAdapter()

    def test_populate_user_with_unique_name(self, adapter):
        request = MagicMock()
        sociallogin = MagicMock()
        data = {"name": "unique_name"}

        user = adapter.populate_user(request, sociallogin, data)
        assert user is not None

    def test_populate_user_with_existing_name(self, adapter):
        UserFactory(name="existing_name")
        request = MagicMock()
        sociallogin = MagicMock()
        sociallogin.account.provider = "github"
        data = {"name": "existing_name"}

        user = adapter.populate_user(request, sociallogin, data)
        assert user is not None

    def test_populate_user_without_name(self, adapter):
        request = MagicMock()
        sociallogin = MagicMock()
        sociallogin.user.username = "testuser"
        data = {}

        user = adapter.populate_user(request, sociallogin, data)
        assert user is not None
