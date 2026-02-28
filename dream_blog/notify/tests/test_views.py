import pytest
from django.conf import settings
from django.shortcuts import resolve_url
from django.urls import reverse

from dream_blog.notify.factories import NotificationFactory
from dream_blog.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_all_notifications_list_requires_login(client):
    url = reverse("notify:notification_all")
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(resolve_url(settings.LOGIN_URL))


def test_unread_notifications_list_requires_login(client):
    url = reverse("notify:notification_unread")
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(resolve_url(settings.LOGIN_URL))


def test_all_notifications_list_authenticated(client):
    user = UserFactory()
    client.force_login(user)
    NotificationFactory.create_batch(5, recipient=user)

    url = reverse("notify:notification_all")
    response = client.get(url)
    assert response.status_code == 200
    assert "notifications" in response.context


def test_unread_notifications_list_authenticated(client):
    user = UserFactory()
    client.force_login(user)
    NotificationFactory.create_batch(3, recipient=user, unread=True)

    url = reverse("notify:notification_unread")
    response = client.get(url)
    assert response.status_code == 200
