from dream_blog.comments import get_form, get_model


def test_get_model():
    from dream_blog.comments.models import Comment

    assert get_model() is Comment


def test_get_form():
    from dream_blog.comments.forms import TreeCommentForm

    assert get_form() is TreeCommentForm
