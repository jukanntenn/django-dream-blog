from django import template

from friendlinks.models import FriendLink

register = template.Library()


@register.inclusion_tag("friendlinks/inclusions/_friendlinks.html")
def show_friendlinks():
    friendlinks = FriendLink.objects.all()
    return {
        "friendlinks": friendlinks,
    }
