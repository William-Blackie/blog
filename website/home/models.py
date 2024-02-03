from django.db import models

from website.utils.models import BasePage
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from website.utils.blocks import ContentStreamField

class HomePage(BasePage):
    template = "pages/home_page.html"

    # Hero
    meta_text = models.CharField(max_length=50, blank=True, null=True)
    introduction = RichTextField(null=True)

    body = StreamField(
        ContentStreamField(),
        null=True, blank=True, use_json_field=True
    )

    content_panels = BasePage.content_panels + [
        # Hero
        FieldPanel("meta_text"),
        FieldPanel("introduction"),
        # Content
        FieldPanel("body"),
    ]
