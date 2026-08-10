import pytest

from dream_blog.comments.forms import TreeCommentForm
from dream_blog.comments.models import Comment
from dream_blog.posts.tests.factories import PostFactory

pytestmark = pytest.mark.django_db


class TestTreeCommentForm:
    @pytest.fixture
    def post(self, user):
        return PostFactory(author=user)

    def test_email_not_required(self, post):
        form = TreeCommentForm(post)
        assert form.fields["email"].required is False

    def test_name_not_required(self, post):
        form = TreeCommentForm(post)
        assert form.fields["name"].required is False

    def test_honeypot_widget_type(self, post):
        form = TreeCommentForm(post)
        assert form.fields["honeypot"].widget.input_type == "hidden"

    def test_parent_field_exists(self, post):
        form = TreeCommentForm(post)
        assert "parent" in form.fields

    def test_get_comment_model(self, post):
        form = TreeCommentForm(post)
        assert form.get_comment_model() is Comment

    def test_init_with_parent(self, user, post):
        from django.contrib.contenttypes.models import ContentType

        ct = ContentType.objects.get_for_model(post)
        parent_comment = Comment.objects.create(
            content_type=ct,
            object_pk=post.pk,
            user=user,
            comment="Parent comment",
            site_id=1,
        )
        form = TreeCommentForm(post, parent=parent_comment)
        assert form.initial.get("parent") == parent_comment.pk

    def test_check_for_duplicate_comment_returns_new(self, post):
        form = TreeCommentForm(post)
        result = form.check_for_duplicate_comment("new_comment")
        assert result == "new_comment"
