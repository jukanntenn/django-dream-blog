from core.models import (
    AlertsModel,
    CommentsModel,
    EntryQuerySet,
    HitCountModel,
    RichContentModel,
    TimeStampedModel,
)
from django.conf import settings
from django.db import models
from django.db.models import Manager
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager
from tags.models import TaggedItem


class PostManager(Manager.from_queryset(EntryQuerySet)):
    pass


class Post(HitCountModel, RichContentModel, TimeStampedModel, CommentsModel, AlertsModel):
    title = models.CharField(_("Title"), max_length=200)
    excerpt = models.TextField(_("Excerpt"), blank=True)
    publish_date = models.DateTimeField(
        _("Publish Date"),
        blank=True,
        null=True,
    )
    hidden = models.BooleanField(_("Hidden"), default=False)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("Author"),
    )
    tags = TaggableManager(
        verbose_name=_("tags"),
        through=TaggedItem,
        blank=True,
    )

    objects = PostManager()

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"pk": self.pk})
