from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from dream_blog.columns.models import Article, Column
from dream_blog.core.admin import EntryAdminMixin


@admin.register(Column)
class ColumnAdmin(EntryAdminMixin, admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "slug",
        "created_at",
        "modified_at",
        "hidden",
        "comments_enabled",
    ]

    search_fields = ["title", "content"]

    prepopulated_fields = {"slug": ("title",)}

    fieldsets = (
        (
            None,
            {
                "fields": ("title", "slug", "excerpt"),
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
                "fields": ("hidden", "comments_enabled"),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Article)
class ArticleAdmin(EntryAdminMixin, admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "hits",
        "publish_date",
        "created_at",
        "modified_at",
        "hidden",
        "comments_enabled",
        "column",
    ]
    list_select_related = ["column"]
    search_fields = ["title"]
    list_filter = ["column"]

    fieldsets = (
        (
            None,
            {
                "fields": ("title", "column", "tags"),
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
