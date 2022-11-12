# Generated by Django 3.2.15 on 2022-11-12 12:40

from django.db import migrations, models
import django.db.models.deletion
import wagtail.blocks
import wagtail.documents.blocks
import wagtail.fields
import website.utils.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtaildocs', '0012_uploadeddocument'),
        ('home', '0003_create_hero'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='body',
            field=wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(template='components/blocks/heading_block.html')), ('paragraph', wagtail.blocks.RichTextBlock(template='components/blocks/paragraph_block.html')), ('image', website.utils.blocks.ImageWithCaptionBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock()), ('code', wagtail.blocks.StructBlock([('code', wagtail.blocks.TextBlock(required=True)), ('language', wagtail.blocks.CharBlock(required=False))])), ('image_text', wagtail.blocks.StructBlock([('image', website.utils.blocks.ImageWithCaptionBlock(required=True)), ('text', wagtail.blocks.RichTextBlock(required=True)), ('alignment', wagtail.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')]))]))], blank=True, null=True, use_json_field=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='cv_file',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtaildocs.document'),
        ),
    ]
