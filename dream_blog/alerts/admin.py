from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.translation import gettext_lazy as _

from alerts.models import Alert


class AlertInline(GenericTabularInline):
    model = Alert
    extra = 0
    fields = ("text", "show", "rank")


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ["id", "text_preview", "show", "rank", "created_at", "modified_at"]
    list_filter = ["show"]
    list_editable = ["show", "rank"]
    search_fields = ["text"]
    ordering = ["rank", "-created_at"]

    def text_preview(self, obj):
        if len(obj.text) > 50:
            return f"{obj.text[:50]}..."
        return obj.text

    text_preview.short_description = _("Text")
