from constance import config
from django import template

register = template.Library()


@register.inclusion_tag("inclusions/_profile.html")
def show_profile():
    profile = {
        "blogger": config.BLOGGER,
        "slogan": config.SLOGAN,
        "social_links": [
            {
                "id": "github",
                "url": config.SOCIAL_LINK_GITHUB,
                "icon": "github-fill.svg",
            },
            {
                "id": "x",
                "url": config.SOCIAL_LINK_X,
                "icon": "twitter-x-fill.svg",
            },
            {
                "id": "telegram",
                "url": config.SOCIAL_LINK_TELEGRAM,
                "icon": "telegram-fill.svg",
            },
            {
                "id": "zhihu",
                "url": config.SOCIAL_LINK_ZHIHU,
                "icon": "zhihu-fill.svg",
            },
            {
                "id": "email",
                "url": config.SOCIAL_LINK_EMAIL,
                "icon": "mail-line.svg",
            },
        ],
    }

    context = {
        "profile": profile,
    }
    return context
