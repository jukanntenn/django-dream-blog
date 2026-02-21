from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from django.db.models import Prefetch
from django.utils.translation import gettext_lazy as _
from markdown_field import MarkdownField
from tree_comments.managers import CommentManager as TreeCommentManager
from tree_comments.models import AbstractComment, AbstractCommentFlag

COMMENT_MAX_LENGTH = getattr(settings, "COMMENT_MAX_LENGTH", 3000)


class CommentManager(TreeCommentManager):
    def threaded_for_instance(self, instance):
        qs = self.cte_for_instance(instance)
        qs = qs.select_related("user", "parent", "parent__user").prefetch_related(
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
        return qs.order_by("-root_id", "submit_date", "id")


class Comment(AbstractComment):
    comment = MarkdownField(_("comment"), max_length=COMMENT_MAX_LENGTH)

    objects = CommentManager()

    class Meta(AbstractComment.Meta):
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = None
        db_table = "tree_comments_treecomment"

    def __str__(self):
        return "%s: %s..." % (self.name, self.comment.text[:50])

    @property
    def is_root(self):
        return self.parent is None

    @property
    def comment_html(self):
        return self.comment.html

    @property
    def anchor(self):
        return f"c{self.pk}"


class CommentFlag(AbstractCommentFlag):
    pass
