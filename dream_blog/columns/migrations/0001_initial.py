# Generated by Django 5.0.2 on 2024-03-03 06:32

import django.db.models.deletion
import django.utils.timezone
import hitcount.models
import model_utils.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Column",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="Created At",
                    ),
                ),
                (
                    "modified_at",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="Modified At",
                    ),
                ),
                ("content", models.TextField(verbose_name="Content")),
                ("title", models.CharField(max_length=150, verbose_name="Title")),
                ("slug", models.SlugField(unique=True, verbose_name="Slug")),
                ("excerpt", models.TextField(blank=True, verbose_name="Excerpt")),
                ("hidden", models.BooleanField(default=False, verbose_name="Hidden")),
                (
                    "comments_enabled",
                    models.BooleanField(default=True, verbose_name="Comments Enabled"),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Author",
                    ),
                ),
            ],
            options={
                "verbose_name": "Column",
                "verbose_name_plural": "Columns",
            },
            bases=(hitcount.models.HitCountMixin, models.Model),
        ),
        migrations.CreateModel(
            name="Article",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="Created At",
                    ),
                ),
                (
                    "modified_at",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="Modified At",
                    ),
                ),
                ("content", models.TextField(verbose_name="Content")),
                (
                    "comments_enabled",
                    models.BooleanField(default=True, verbose_name="Comments Enabled"),
                ),
                ("title", models.CharField(max_length=200, verbose_name="Title")),
                (
                    "publish_date",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Publish Date"
                    ),
                ),
                ("hidden", models.BooleanField(default=False, verbose_name="Hidden")),
                (
                    "column",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="columns.column",
                        verbose_name="Column",
                    ),
                ),
            ],
            options={
                "verbose_name": "Article",
                "verbose_name_plural": "Articles",
            },
            bases=(hitcount.models.HitCountMixin, models.Model),
        ),
    ]