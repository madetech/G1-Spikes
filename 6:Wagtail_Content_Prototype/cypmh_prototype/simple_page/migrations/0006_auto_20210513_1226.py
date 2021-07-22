# Generated by Django 3.1.8 on 2021-05-13 12:26

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('simple_page', '0005_simplepage_image_block'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simplepage',
            name='image_block',
            field=wagtail.core.fields.StreamField([('image_block', wagtail.core.blocks.StreamBlock([('image', wagtail.images.blocks.ImageChooserBlock())]))], blank=True),
        ),
    ]