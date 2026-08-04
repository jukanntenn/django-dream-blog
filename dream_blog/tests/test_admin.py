import pytest
from django.contrib.admin.sites import AdminSite

pytestmark = pytest.mark.django_db


class TestSubscriptionAdmin:
    def test_get_readonly_fields_new(self):
        from dream_blog.newsletters.admin import SubscriptionAdmin
        from dream_blog.newsletters.models import Subscription

        site = AdminSite()
        admin = SubscriptionAdmin(Subscription, site)
        fields = admin.get_readonly_fields(request=None, obj=None)
        assert "email" not in fields

    def test_get_readonly_fields_existing(self):
        from dream_blog.newsletters.admin import SubscriptionAdmin
        from dream_blog.newsletters.models import Subscription

        site = AdminSite()
        admin = SubscriptionAdmin(Subscription, site)
        sub = Subscription(email="test@example.com")
        fields = admin.get_readonly_fields(request=None, obj=sub)
        assert "email" in fields
