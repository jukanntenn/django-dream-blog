from django import template

register = template.Library()


@register.inclusion_tag("share/_share_icons.html", takes_context=True)
def share_icons(context, entry):
    return {
        "entry": entry,
        "request": context.get("request"),
    }
