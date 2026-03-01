from django.contrib import admin

from .models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ["email", "user", "confirmed", "active", "created_at"]
    list_filter = ["confirmed", "active"]
    search_fields = ["email"]
    readonly_fields = ["created_at", "modified_at"]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [*self.readonly_fields, "email"]
        return self.readonly_fields
