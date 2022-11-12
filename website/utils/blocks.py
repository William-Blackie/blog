from wagtail import blocks
from django.forms.utils import ErrorList
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from os import listdir
from os.path import isfile, join

class InternalExternalLinkBlock(blocks.StructBlock):
    """
    A block that allows you to choose between an internal or external link.
    """
    internal_link = blocks.PageChooserBlock(required=False)
    external_link = blocks.URLBlock(required=False)

    class Meta:
        icon = 'link'
        template = 'utils/blocks/internal_external_link.html'

    @property
    def link(self):
        if self.value.get('internal_link'):
            return self.value.get('internal_link').url
        return self.value.get('external_link')

    def clean(self, value):
        errors = {}
        if value.get('internal_link') and value.get('external_link'):
            msg =  'Only one of these fields should be filled out.'
            errors['internal_link'] = ErrorList([
                msg
            ])
            errors['external_link'] = ErrorList([
                msg
            ])

        if not value.get('internal_link') and not value.get('external_link'):
            msg = 'You must fill out one of these fields.'
            errors['internal_link'] = ErrorList([
                msg
            ])
            errors['external_link'] = ErrorList([
                msg
            ])

        if errors:
            raise ValidationError('Validation error in InternalExternalLinkBlock', params=errors)

        return super(InternalExternalLinkBlock, self).clean(value)


class CardBlock(blocks.StructBlock):
    """
    A card block with an image, title, and link.
    """
    title = blocks.CharBlock(required=True)
    text = blocks.RichTextBlock(required=True)
    link = InternalExternalLinkBlock(required=True)
    image = ImageChooserBlock(required=False)

    class Meta:
        icon = 'placeholder'
        template = 'components/blocks/card.html'


class ProjectCardBlock(CardBlock):
    """
    A card block with an link.
    """
    github_link = blocks.URLBlock(required=False)

    class Meta:
        icon = 'placeholder'
        template = 'components/blocks/project_card.html'

class ProjectsCardBlock(CardBlock):
    """
    This is a custom block for the homepage. It is a card with a list of projects.
    """
    project_cards = StreamField(
        [
            ('project', ProjectCardBlock()),
        ],
        null=True,
        blank=True,
    )

    class Meta:
        icon = 'placeholder'
        template = 'components/blocks/projects_card.html'

class ImageWithCaptionBlock(ImageChooserBlock):
    """
    A ImageChooserBlock with caption and alt text.
    """
    caption = blocks.CharBlock(required=False)
    alt_text = blocks.CharBlock(required=True)

    class Meta:
        icon = 'image'

class CodeBlock(blocks.StructBlock):
    """
    A block for code snippets.
    """
    code = blocks.TextBlock(required=True)
    language = blocks.CharBlock(required=False)

    class Meta:
        icon = 'code'
        template = 'components/blocks/code_block.html'

class ImageTextBlock(blocks.StructBlock):
    """
    A block for an image with text.
    """
    image = ImageWithCaptionBlock(required=True)
    text = blocks.RichTextBlock(required=True)
    alignment = blocks.ChoiceBlock(
        choices=[
            ('left', 'Left'),
            ('right', 'Right'),
        ],
        default='left',
        required=True,
    )

    class Meta:
        icon = 'placeholder'
        template = 'components/blocks/image_text_block.html'


class ContentStreamField(blocks.StreamBlock):
    """"
    A StreamField that contains all the blocks that can be used in the general content.
    """
    heading = blocks.CharBlock(
        template='components/blocks/heading_block.html',
    )
    paragraph = blocks.RichTextBlock(
        template="components/blocks/paragraph_block.html"
    )
    image = ImageWithCaptionBlock()
    document = DocumentChooserBlock()
    code = CodeBlock()
    image_text = ImageTextBlock()
    
    class Meta:
        template = 'components/blocks/content.html'
