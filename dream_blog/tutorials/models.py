from core.models import (
    CommentsModel,
    EntryQuerySet,
    HitCountModel,
    RichContentModel,
    TimeStampedModel,
)
from django.conf import settings
from django.db import models
from django.db.models import Manager, QuerySet
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from model_utils.choices import Choices


class Category(TimeStampedModel):
    name = models.CharField(_("Name of Category"), max_length=50)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


class TutorialQuerySet(QuerySet):
    def visible(self):
        return self.filter(hidden=False)


class TutoriallManager(Manager.from_queryset(TutorialQuerySet)):
    pass


class Tutorial(HitCountModel, RichContentModel, TimeStampedModel):
    STATUS = Choices(
        (1, "writing", _("Writing")),
        (2, "completed", _("Completed")),
        (3, "outdated", _("Outdated")),
    )

    title = models.CharField(_("Title"), max_length=150)
    slug = models.SlugField(_("Slug"), unique=True)
    excerpt = models.TextField(_("Excerpt"), blank=True)
    status = models.IntegerField(_("Status"), choices=STATUS, default=STATUS.writing)
    hidden = models.BooleanField(_("Hidden"), default=False)
    comments_enabled = models.BooleanField(_("Comments Enabled"), default=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Author"),
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        Category,
        verbose_name=_("Category"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    objects = TutoriallManager()

    class Meta:
        verbose_name = _("Tutorial")
        verbose_name_plural = _("Tutorials")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("tutorials:detail", kwargs={"slug": self.slug})


class MaterialQuerySet(EntryQuerySet):
    def visible(self):
        return super().visible().filter(tutorial__hidden=False)


class MaterialManager(Manager.from_queryset(MaterialQuerySet)): ...


class Material(HitCountModel, RichContentModel, TimeStampedModel, CommentsModel):
    title = models.CharField(_("Title"), max_length=200)
    publish_date = models.DateTimeField(
        _("Publish Date"),
        blank=True,
        null=True,
    )
    hidden = models.BooleanField(_("Hidden"), default=False)

    tutorial = models.ForeignKey(
        Tutorial,
        verbose_name=_("Tutorial"),
        on_delete=models.CASCADE,
    )

    objects = MaterialManager()

    class Meta:
        verbose_name = _("Material")
        verbose_name_plural = _("Materials")

    def __str__(self):
        return self.title

    @property
    def author(self):
        return self.tutorial.author

    def get_absolute_url(self):
        return reverse(
            "tutorials:material_detail",
            kwargs={"slug": self.tutorial.slug, "pk": self.pk},
        )
