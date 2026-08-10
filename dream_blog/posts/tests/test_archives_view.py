from datetime import timedelta

import pytest
from django.utils import timezone
from django.utils.text import slugify
from test_plus.plugin import TestCase

from dream_blog.columns.models import Article, Column
from dream_blog.core.templatetags.entry_urls import entry_url
from dream_blog.posts.tests.factories import PostFactory
from dream_blog.tutorials.tests.factories import MaterialFactory, TutorialFactory
from dream_blog.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_archives_view_is_good(tp: TestCase):
    response = tp.get_check_200("archives")
    tp.assertTemplateUsed(response, "posts/archives.html")


def test_archives_view_displays_visible_entries(tp: TestCase):
    post = PostFactory(title="Test Post", publish_date=timezone.now() - timedelta(days=30))
    material = MaterialFactory(
        title="Test Material",
        publish_date=timezone.now() - timedelta(days=15),
    )

    response = tp.get_check_200("archives")
    tp.assertContains(response, post.title)
    tp.assertContains(response, material.title)


def test_archives_view_hides_invisible_entries(tp: TestCase):
    hidden_post = PostFactory(
        title="Hidden Post",
        publish_date=timezone.now() - timedelta(days=1),
        hidden=True,
    )
    future_post = PostFactory(
        title="Future Post",
        publish_date=timezone.now() + timedelta(days=1),
        hidden=False,
    )
    hidden_material = MaterialFactory(
        title="Hidden Material",
        publish_date=timezone.now() - timedelta(days=1),
        hidden=True,
    )

    response = tp.get_check_200("archives")
    tp.assertNotContains(response, hidden_post.title)
    tp.assertNotContains(response, future_post.title)
    tp.assertNotContains(response, hidden_material.title)


def test_archives_view_context_has_entries(tp: TestCase):
    PostFactory(publish_date=timezone.now() - timedelta(days=1))
    response = tp.get_check_200("archives")
    assert "entries" in response.context


def test_archives_view_entry_urls_are_valid(tp: TestCase):
    PostFactory(publish_date=timezone.now() - timedelta(days=5))
    MaterialFactory(publish_date=timezone.now() - timedelta(days=3))

    response = tp.get_check_200("archives")
    entries = response.context["entries"]

    for entry in entries:
        url = entry_url(entry)
        entry_response = tp.client.get(url)
        assert entry_response.status_code in (200, 301, 302)


def test_archives_integration_multiple_entry_types(tp: TestCase):
    user = UserFactory()
    column = Column.objects.create(
        title="Test Column",
        slug=slugify("Test Column"),
        excerpt="",
        content="Test column content",
        author=user,
        hidden=False,
    )
    Article.objects.create(
        title="Test Article",
        content="Test article content",
        publish_date=timezone.now() - timedelta(days=20),
        hidden=False,
        column=column,
    )

    tutorial = TutorialFactory(title="Test Tutorial")
    MaterialFactory(
        title="Test Material",
        tutorial=tutorial,
        publish_date=timezone.now() - timedelta(days=10),
        hidden=False,
    )

    PostFactory(title="Test Post", publish_date=timezone.now() - timedelta(days=5), hidden=False)

    response = tp.get_check_200("archives")
    content = response.content.decode()

    assert "Test Post" in content
    assert "Test Article" in content
    assert "Test Material" in content
    assert "Test Column" in content
    assert "Test Tutorial" in content
