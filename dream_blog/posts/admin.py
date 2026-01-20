from core.admin import hide, show
from django.contrib import admin
from markdown_field.widgets import PreviewMarkdownWidget
from markdown_field.fields import MarkdownField
from posts.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    actions = [hide, show]
    date_hierarchy = "publish_date"
    list_display = [
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

    formfield_overrides = {
        MarkdownField: {"widget": PreviewMarkdownWidget}
    }

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "excerpt",
                    "content",
                    "comments_enabled",
                    "hidden",
                    "publish_date",
                )
            },
        ),
    )
    search_fields = ["title", "content"]
    list_select_related = ["author"]

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)
