from django.contrib import admin
from django.utils.translation import gettext_lazy as _


@admin.action(description=_("Hide selected %(verbose_name_plural)s"))
def hide(modeladmin, request, queryset):
    queryset.update(hidden=True)


@admin.action(description=_("Show selected %(verbose_name_plural)s"))
def show(modeladmin, request, queryset):
    queryset.update(hidden=False)
