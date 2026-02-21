from comments.forms import TreeCommentForm
from comments.models import Comment
from django import template

register = template.Library()


@register.inclusion_tag("comments/inclusions/_comment_app.html", takes_context=True)
def show_comment_app(context, target):
    comments = Comment.objects.threaded_for_instance(target)

    return {
        "form": TreeCommentForm(target_object=target),
        "tree_comments": comments,
        "comment_count": target.comment_count,
        # Must pass explicitly
        "user": context["user"],
        "request": context["request"],
    }
