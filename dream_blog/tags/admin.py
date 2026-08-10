from django.contrib import admin

from dream_blog.tags.models import Tag, TaggedItem


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "created_at", "modified_at")
    list_display_links = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug")


@admin.register(TaggedItem)
class TaggedItemAdmin(admin.ModelAdmin):
    list_display = ("id", "tag", "content_type", "object_id", "created_at")
    list_filter = ("tag", "content_type")
