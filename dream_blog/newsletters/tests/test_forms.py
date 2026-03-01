import pytest

from dream_blog.newsletters.forms import SubscriptionForm
from dream_blog.newsletters.models import Subscription
from dream_blog.users.tests.factories import UserFactory


@pytest.mark.django_db
class TestSubscriptionForm:
    def test_valid_email(self):
        form = SubscriptionForm(data={"email": "test@example.com"})
        assert form.is_valid()

    def test_duplicate_confirmed_email(self):
        Subscription.objects.create(email="test@example.com", confirmed=True, active=True)
        form = SubscriptionForm(data={"email": "test@example.com"})
        assert not form.is_valid()
        assert "already subscribed" in str(form.errors).lower()

    def test_unconfirmed_subscription_replaced(self):
        Subscription.objects.create(email="test@example.com", confirmed=False)
        form = SubscriptionForm(data={"email": "test@example.com"})
        assert form.is_valid()
        form.save()
        assert Subscription.objects.filter(email="test@example.com").count() == 1

    def test_save_with_authenticated_user(self):
        user = UserFactory()
        form = SubscriptionForm(data={"email": "test@example.com"}, user=user)
        assert form.is_valid()
        sub = form.save()
        assert sub.user == user
