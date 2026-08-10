def get_model():
    from dream_blog.comments.models import Comment

    return Comment


def get_form():
    from dream_blog.comments.forms import TreeCommentForm

    return TreeCommentForm
