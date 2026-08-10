import pytest

from dream_blog.comments.models import Comment

pytestmark = pytest.mark.django_db


class TestComment:
    @pytest.fixture
    def comment(self, user, post):
        from django.contrib.contenttypes.models import ContentType

        ct = ContentType.objects.get_for_model(post)
        return Comment.objects.create(
            content_type=ct,
            object_pk=post.pk,
            user=user,
            comment="Test comment content",
            site_id=1,
        )

    def test_str(self, comment):
        expected = "%s: %s..." % (comment.name, comment.comment.text[:50])
        assert str(comment) == expected

    def test_is_root_when_no_parent(self, comment):
        assert comment.is_root is True

    def test_is_not_root_with_parent(self, user, post, comment):
        from django.contrib.contenttypes.models import ContentType

        ct = ContentType.objects.get_for_model(post)
        child = Comment.objects.create(
            content_type=ct,
            object_pk=post.pk,
            user=user,
            comment="Child comment",
            parent=comment,
            site_id=1,
        )
        assert child.is_root is False

    def test_comment_html(self, comment):
        assert comment.comment.html is not None

    def test_anchor(self, comment):
        assert comment.anchor == f"c{comment.pk}"
