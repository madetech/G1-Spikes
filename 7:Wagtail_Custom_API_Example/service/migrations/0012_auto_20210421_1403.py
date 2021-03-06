# Generated by Django 3.1.8 on 2021-04-21 14:03

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('service', '0011_auto_20210421_1328'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='service.service')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_servicetag_items', to='taggit.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='service',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='service.ServiceTag', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
