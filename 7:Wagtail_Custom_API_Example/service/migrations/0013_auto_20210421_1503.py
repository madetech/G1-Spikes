# Generated by Django 3.1.8 on 2021-04-21 15:03

from django.db import migrations
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0012_auto_20210421_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicetag',
            name='content_object',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='serviceTags', to='service.service'),
        ),
    ]
