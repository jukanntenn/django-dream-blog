import pytest

from dream_blog.core.utils import EmailConfirmation
from dream_blog.users.tests.factories import UserFactory


@pytest.mark.django_db
class TestEmailConfirmation:
    def test_make_key_returns_signed_token(self):
        user = UserFactory(email="test@example.com")
        confirmation = EmailConfirmation(user)
        key = confirmation.make_key()

        assert isinstance(key, str)
        assert key

    def test_from_key_with_valid_key(self):
        user = UserFactory(email="test@example.com")
        key = EmailConfirmation(user).make_key()

        restored = EmailConfirmation.from_key(key)

        assert restored is not None
        assert restored.instance.pk == user.pk

    def test_from_key_with_invalid_key(self):
        restored = EmailConfirmation.from_key("invalid-key")

        assert restored is None
