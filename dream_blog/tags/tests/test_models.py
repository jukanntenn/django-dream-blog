import pytest

from dream_blog.tags.tests.factories import TagFactory

pytestmark = pytest.mark.django_db


class TestTag:
    def test_str(self):
        tag = TagFactory(name="django")
        assert str(tag) == "django"

    def test_slug_autofilled(self):
        tag = TagFactory(name="python")
        assert tag.slug == "python"


class TestTaggedItem:
    def test_add_tag_to_post(self, post):
        tag = TagFactory(name="python")
        post.tags.add(tag)
        assert post.tags.count() == 1
        assert post.tags.first().name == "python"

    def test_add_tag_to_tutorial(self, tutorial):
        tag = TagFactory(name="django")
        tutorial.tags.add(tag)
        assert tutorial.tags.count() == 1
        assert tutorial.tags.first().name == "django"
