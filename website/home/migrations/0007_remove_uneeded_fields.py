# Generated by Django 3.2.15 on 2022-12-10 20:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_create_base_page'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepage',
            name='cv_file',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='hero_image',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='image_meta_text',
        ),
    ]
