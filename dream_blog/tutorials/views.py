from hitcount.views import HitCountDetailView

from dream_blog.core.views import SetHeadlineMixin
from dream_blog.tutorials.models import Material, Tutorial


class TutorialDetailView(SetHeadlineMixin, HitCountDetailView):
    model = Tutorial
    count_hit = True
    template_name = "tutorials/detail.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return Tutorial.objects.visible().select_related("category").order_by("-created_at")

    def get_headline(self):
        return self.object.title


class MaterialDetailView(SetHeadlineMixin, HitCountDetailView):
    model = Material
    count_hit = True
    template_name = "tutorials/material_detail.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return Material.objects.visible().select_related("tutorial").order_by("publish_date").with_comment_count()

    def get_headline(self):
        return f"{self.object.title} - {self.object.tutorial.title}"
