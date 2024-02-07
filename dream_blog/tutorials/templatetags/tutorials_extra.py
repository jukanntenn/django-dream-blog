from django import template
from django.utils import timezone
from tutorials.models import Tutorial

register = template.Library()


@register.inclusion_tag(
    "tutorials/inclusions/_tutorials.html",
)
def show_tutorials(num=5):
    tutorials = (
        Tutorial.objects.filter(hidden=False)
        .select_related("category")
        .order_by("-created_at")[:num]
    )
    return {"tutorials": tutorials}


@register.inclusion_tag("tutorials/inclusions/_toc.html")
def show_tutorial_toc(tutorial, current=None):
    materials = (
        tutorial.material_set.filter(
            hidden=False,
            publish_date__isnull=False,
            publish_date__lt=timezone.now(),
        )
        .order_by("publish_date")
        .values("id", "title")
    )

    context = {
        "tutorial": tutorial,
        "materials": materials,
        "current": current,
    }
    return context
