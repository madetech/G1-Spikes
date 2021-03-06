# Generated by Django 3.1.8 on 2021-05-14 10:57

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0062_comment_models_and_pagesubscription'),
    ]

    operations = [
        migrations.CreateModel(
            name='NHSPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('body', wagtail.core.fields.StreamField([('action_link', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock(label='Link text', required=True)), ('external_url', wagtail.core.blocks.URLBlock(label='URL', required=False)), ('new_window', wagtail.core.blocks.BooleanBlock(label='Open in new window', required=False)), ('internal_page', wagtail.core.blocks.PageChooserBlock(label='Internal Page', required=False))])), ('callout', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(default='Important', required=True)), ('visually_hidden_prefix', wagtail.core.blocks.BooleanBlock(help_text='If the title doesn\'t contain the word "Important" select this to add a visually hidden "Important", to aid screen readers.', label='Visually hidden prefix', required=False)), ('heading_level', wagtail.core.blocks.IntegerBlock(default=3, help_text='The heading level affects users with screen readers. Default=3, Min=2, Max=6.', max_value=6, min_value=2, required=True)), ('body', wagtail.core.blocks.RichTextBlock(required=True))]))])),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
