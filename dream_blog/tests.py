from datetime import timedelta

import pytest
from django.utils import timezone
from posts.tests.factories import PostFactory
from users.tests.factories import UserFactory

from dream_blog.views import HomeView

pytestmark = pytest.mark.django_db


def test_home_view_is_good(tp):
    response = tp.get_check_200("home")
    tp.assertTemplateUsed(response, "pages/home.html")
    tp.assertContains(response, "追梦人物的博客")


def test_home_posts_ordering(tp):
    author = UserFactory()

    now = timezone.now()
    p0 = PostFactory(publish_date=now - timedelta(days=3), author=author)
    p1 = PostFactory(publish_date=now - timedelta(days=1), author=author)

    view = HomeView()
    qs = view.get_queryset()
    tp.assertQuerySetEqual(qs, [p1, p0])
