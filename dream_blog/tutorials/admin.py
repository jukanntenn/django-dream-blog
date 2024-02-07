from core.admin import hide, show
from django.contrib import admin
from tutorials.models import Category, Material, Tutorial


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    actions = [hide, show]
    list_display = [
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

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "slug",
                    "excerpt",
                    "content",
                    "status",
                    "hidden",
                    "comments_enabled",
                    "category",
                )
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    actions = [hide, show]
    list_display = [
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
