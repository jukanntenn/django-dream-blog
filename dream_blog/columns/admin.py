from columns.models import Article, Column
from core.admin import hide, show
from django.contrib import admin


@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    actions = [hide, show]
    list_display = [
        "title",
        "slug",
        "created_at",
        "modified_at",
        "hidden",
        "comments_enabled",
    ]

    search_fields = ["title", "content"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "slug",
                    "excerpt",
                    "content",
                    "hidden",
                    "comments_enabled",
                )
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    actions = [hide, show]
    list_display = [
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
