from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

class HomePage(Page):
    template="pages/home_page.html"

    # Hero
    hero_image = models.ForeignKey(
        "images.CustomImage",
        models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    image_meta_text = models.CharField(max_length=50, blank=True, null=True)
    meta_text = models.CharField(max_length=50, blank=True, null=True)
    introduction = RichTextField(null=True)
    
    content_panels = Page.content_panels + [
        FieldPanel("hero_image"),
        FieldPanel("image_meta_text"),
        FieldPanel("meta_text"),
        FieldPanel("introduction")
    ]
