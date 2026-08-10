from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from markdown_field.fields import MarkdownField
from markdown_field.widgets import PreviewMarkdownWidget

from dream_blog.alerts.admin import AlertInline


@admin.action(description=_("Hide selected %(verbose_name_plural)s"))
def hide(modeladmin, request, queryset):
    queryset.update(hidden=True)


@admin.action(description=_("Show selected %(verbose_name_plural)s"))
def show(modeladmin, request, queryset):
    queryset.update(hidden=False)


class MarkdownContentAdminMixin:
    """Provides the markdown preview widget for content admin forms."""

    formfield_overrides = {MarkdownField: {"widget": PreviewMarkdownWidget}}


class EntryAdminMixin(MarkdownContentAdminMixin):
    """Shared behaviour for blog content entries: bulk visibility actions and alert inlines."""

    actions = [hide, show]
    inlines = [AlertInline]
