from datetime import datetime, timedelta

import pytest
from freezegun import freeze_time
from posts.models import Post
from posts.tests.factories import PostFactory
from test_plus.plugin import TestCase

pytestmark = pytest.mark.django_db


def test_post_detail_view_is_good(tp: TestCase, post: Post):
    response = tp.get_check_200("posts:detail", pk=post.pk)
    tp.assertTemplateUsed(response, "posts/detail.html")


def test_post_detail_view_headline(tp: TestCase, post: Post):
    response = tp.get_check_200("posts:detail", pk=post.pk)
    tp.assertContains(response, f"{post.title} - 追梦人物的博客")


def test_post_detail_view_hits(tp: TestCase, post: Post):
    assert post.hits == 0

    tp.get_check_200("posts:detail", pk=post.pk)
    post.refresh_from_db()
    assert post.hits == 1

    with freeze_time(lambda: datetime.now() + timedelta(minutes=1)):
        tp.get_check_200("posts:detail", pk=post.pk)

    post.refresh_from_db()
    assert post.hits == 2


def test_can_not_see_invisible_post(tp: TestCase):
    post = PostFactory(hidden=True)
    response = tp.get("posts:detail", pk=post.pk)
    tp.assert_http_404_not_found(response)
