from website.utils.blocks import ContentStreamField
from website.utils.models import BasePage
from wagtail.core.fields import StreamField
from django.db import models
from wagtail.admin.panels import FieldPanel

class BlogIndexPage(BasePage):
    template = "pages/blog_index_page.html"
    child_page_types = ['BlogPage']
    body = StreamField(
        ContentStreamField(),
        null=True, blank=True, use_json_field=True 
    )

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        context['blog_pages'] = self.get_children().live().order_by('-first_published_at')
        return context

    class Meta:
        verbose_name = "Blog Index Page"

class BlogPage(BasePage):
    template = "pages/blog_page.html"
    parent_page_types = ['BlogIndexPage']
    date = models.DateField("Post date")
    body = StreamField(
        ContentStreamField(),
        use_json_field=True 
    )

    content_panels = BasePage.content_panels + [
        FieldPanel('date'),
        FieldPanel('body', classname="full"),
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        context['blog_pages'] = self.get_children().live().order_by('-first_published_at')
        return context

    class Meta:
        verbose_name = "Blog Page"