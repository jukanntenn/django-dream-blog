from django.contrib import admin

from .models import Favorite, Issue


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ["number", "pub_date", "description"]
    fields = ["number", "pub_date", "description", "creator", "tags"]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator = request.user
        super().save_model(request, obj, form, change)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ["rank", "title", "issue", "url"]
    list_filter = ["issue"]
    fields = ["issue", "title", "description", "url", "rank", "tags"]
