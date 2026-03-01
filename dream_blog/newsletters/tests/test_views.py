import pytest
from django.core import mail
from django.urls import reverse

from dream_blog.core.utils import EmailConfirmation
from dream_blog.newsletters.models import Subscription


@pytest.mark.django_db
class TestSubscriptionCreateView:
    def test_view_resolves(self, client):
        url = reverse("newsletters:subscription")
        response = client.get(url)
        assert response.status_code == 200

    def test_valid_subscription_sends_email(self, client, settings):
        settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
        response = client.post(reverse("newsletters:subscription"), {"email": "test@example.com"})
        assert response.status_code == 302
        assert Subscription.objects.filter(email="test@example.com").exists()
        assert len(mail.outbox) == 1
        assert "test@example.com" in mail.outbox[0].to


@pytest.mark.django_db
class TestSubscriptionConfirmView:
    def test_valid_confirmation(self, client):
        sub = Subscription.objects.create(email="test@example.com")
        key = EmailConfirmation(sub).make_key()

        url = reverse("newsletters:subscription-confirm", kwargs={"key": key})
        response = client.get(url)

        assert response.status_code == 302
        sub.refresh_from_db()
        assert sub.confirmed
        assert sub.active

    def test_invalid_confirmation(self, client):
        url = reverse("newsletters:subscription-confirm", kwargs={"key": "invalid-key"})
        response = client.get(url)
        assert response.status_code == 302
