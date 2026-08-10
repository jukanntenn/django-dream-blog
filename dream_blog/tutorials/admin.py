from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from dream_blog.core.admin import EntryAdminMixin
from dream_blog.tutorials.models import Category, Material, Tutorial


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Tutorial)
class TutorialAdmin(EntryAdminMixin, admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "slug",
        "status",
        "created_at",
        "modified_at",
        "hidden",
        "comments_enabled",
        "category",
    ]
    list_select_related = ["category"]

    search_fields = ["title", "content"]
    list_filter = ["category"]

    prepopulated_fields = {"slug": ("title",)}

    fieldsets = (
        (
            None,
            {
                "fields": ("title", "slug", "excerpt", "category", "tags"),
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
                "fields": ("status", "hidden", "comments_enabled"),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Material)
class MaterialAdmin(EntryAdminMixin, admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "hits",
        "publish_date",
        "created_at",
        "modified_at",
        "hidden",
        "comments_enabled",
        "tutorial",
    ]
    list_select_related = ["tutorial"]
    search_fields = ["title"]
    list_filter = ["tutorial"]
    readonly_fields = ["created_at", "modified_at"]

    fieldsets = (
        (
            None,
            {
                "fields": ("title", "tutorial"),
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
        (
            _("System"),
            {
                "fields": ("created_at", "modified_at"),
            },
        ),
    )
