# Generated by Django 3.1.8 on 2021-04-21 12:56

from django.db import migrations, models
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_auto_20210421_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicepage',
            name='description',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='servicepage',
            name='maxAge',
            field=models.PositiveIntegerField(default=100),
        ),
        migrations.AddField(
            model_name='servicepage',
            name='minAge',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
