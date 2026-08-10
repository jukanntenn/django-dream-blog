from django.contrib import admin
from django_comments.admin import CommentsAdmin

from dream_blog.comments.models import Comment


@admin.register(Comment)
class TreeCommentsAdmin(CommentsAdmin):
    list_display = (
        "user_name",
        "parent_id",
        "content_type",
        "object_pk",
        "ip_address",
        "submit_date",
        "is_public",
        "is_removed",
    )
    list_select_related = ["user"]
