from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from dream_blog.core.admin import EntryAdminMixin
from dream_blog.posts.models import Post


@admin.register(Post)
class PostAdmin(EntryAdminMixin, admin.ModelAdmin):
    date_hierarchy = "publish_date"
    list_display = [
        "id",
        "title",
        "hits",
        "publish_date",
        "created_at",
        "modified_at",
        "hidden",
        "comments_enabled",
        "author",
    ]
    list_filter = [
        "hidden",
        "comments_enabled",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": ("title", "excerpt", "tags"),
            },
        ),
        (
            _("Content"),
            {
                "fields": ("content",),
            },
        ),
        (
            _("Publishing"),
            {
                "fields": ("publish_date", "hidden", "comments_enabled"),
            },
        ),
    )
    search_fields = ["title", "content"]
    list_select_related = ["author"]

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)
