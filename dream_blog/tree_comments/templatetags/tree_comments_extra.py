from allauth.socialaccount.models import SocialAccount
from django import template
from django.db.models import F, Prefetch
from django_cte import With
from tree_comments.forms import TreeCommentForm
from tree_comments.models import TreeComment

register = template.Library()


def _microsecond(dt):
    return int(dt.timestamp() * 1e6)


def _sort_key(comment):
    root_ts = _microsecond(comment.root_submit_date)
    self_ts = _microsecond(comment.submit_date)

    primary = -int(f"{root_ts}_{comment.root_pk}")
    secondary = f"{self_ts}_{comment.pk}"

    return (primary, secondary)


@register.inclusion_tag(
    "tree_comments/inclusions/_comment_app.html", takes_context=True
)
def show_comment_app(context, target):
    def make_comments_cte(cte):
        return (
            TreeComment.objects.for_model(target)
            .roots()
            # .select_related("user", "parent", "parent__user")
            .annotate(root_pk=F("pk"), root_submit_date=F("submit_date"))
            .union(
                cte.join(TreeComment, parent=cte.col.id)
                # .select_related("user", "parent", "parent__user")
                .annotate(
                    root_pk=cte.col.root_pk,
                    root_submit_date=cte.col.root_submit_date,
                ),
                all=True,
            )
        )

    cte = With.recursive(make_comments_cte)
    comments = (
        cte.join(TreeComment, id=cte.col.id)
        .with_cte(cte)
        .select_related("user", "parent", "parent__user")
        .prefetch_related(
            Prefetch(
                "user__socialaccount_set",
                queryset=SocialAccount.objects.all(),
                to_attr="socialaccounts",
            ),
            Prefetch(
                "parent__user__socialaccount_set",
                queryset=SocialAccount.objects.all(),
                to_attr="socialaccounts",
            ),
        )
        .annotate(
            root_pk=cte.col.root_pk,
            root_submit_date=cte.col.root_submit_date,
        )
    )
    comments = sorted(comments, key=_sort_key)

    return {
        "form": TreeCommentForm(target_object=target),
        "tree_comments": comments,
        "comment_count": target.comment_count,
        # Must pass explicitly
        "user": context["user"],
        "request": context["request"],
    }
