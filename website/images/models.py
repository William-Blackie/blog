from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from wagtail.images.models import AbstractImage, AbstractRendition


class CustomImage(AbstractImage):
    alternative_text = models.CharField(
        max_length=255,
        blank=True,
        help_text="Alternative text for the image, for visually impaired users",
    )

    admin_form_fields = (
        "title",
        "file",
        "tags",
        "focal_point_x",
        "focal_point_y",
        "focal_point_width",
        "focal_point_height",
    )

class CustomRendition(AbstractRendition):
    image = models.ForeignKey(
        "CustomImage", models.CASCADE, related_name="renditions"
    )

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)