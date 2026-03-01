from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager

from dream_blog.core.models import TimeStampedModel


class Issue(TimeStampedModel):
    number = models.PositiveSmallIntegerField(_("number"), unique=True)
    pub_date = models.DateTimeField(_("publication datetime"))
    description = models.TextField(_("description"))
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("creator"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    tags = TaggableManager(verbose_name=_("tags"), blank=True)

    class Meta:
        ordering = ["-number"]
        verbose_name = _("issue")
        verbose_name_plural = _("issues")

    def __str__(self) -> str:
        return f"Issue #{self.number}"

    def get_absolute_url(self) -> str:
        return reverse("favorites:issue_detail", kwargs={"number": self.number})


class Favorite(TimeStampedModel):
    issue = models.ForeignKey(
        Issue,
        verbose_name=_("issue"),
        on_delete=models.CASCADE,
        related_name="favorites",
    )
    title = models.CharField(_("title"), max_length=200)
    description = models.TextField(_("description"), blank=True)
    url = models.URLField(_("url"))
    rank = models.IntegerField(_("rank"), default=0)
    tags = TaggableManager(verbose_name=_("tags"), blank=True)

    class Meta:
        ordering = ["rank", "-created_at"]
        verbose_name = _("favorite")
        verbose_name_plural = _("favorites")

    def __str__(self) -> str:
        return self.title
