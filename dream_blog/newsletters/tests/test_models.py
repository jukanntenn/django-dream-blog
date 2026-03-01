import pytest
from django.db import IntegrityError

from dream_blog.newsletters.models import Subscription


@pytest.mark.django_db
class TestSubscription:
    def test_subscription_creation(self):
        sub = Subscription.objects.create(email="test@example.com")
        assert str(sub) == "test@example.com"
        assert not sub.confirmed
        assert not sub.active

    def test_confirm_method(self):
        sub = Subscription.objects.create(email="test@example.com")
        sub.confirm()
        sub.refresh_from_db()
        assert sub.confirmed
        assert sub.active

    def test_unique_confirmed_email(self):
        Subscription.objects.create(email="test@example.com", confirmed=True, active=True)
        with pytest.raises(IntegrityError):
            Subscription.objects.create(email="test@example.com", confirmed=True, active=True)
