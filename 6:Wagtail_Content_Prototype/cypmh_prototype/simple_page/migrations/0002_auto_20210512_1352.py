# Generated by Django 3.1.10 on 2021-05-12 13:52

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0060_fix_workflow_unique_constraint'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wagtailforms', '0004_add_verbose_name_plural'),
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('simple_page', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Service',
            new_name='SimplePage',
        ),
    ]