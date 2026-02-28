from django import template
from friendlinks.models import FriendLink

register = template.Library()


@register.inclusion_tag("friendlinks/inclusions/_friendlinks.html")
def show_friendlinks(num=10):
    friendlinks = FriendLink.objects.all()[:num]
    return {
        "friendlinks": friendlinks,
    }
