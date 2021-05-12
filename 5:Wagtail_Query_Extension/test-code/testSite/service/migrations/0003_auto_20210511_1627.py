# Generated by Django 3.1.8 on 2021-05-11 16:27

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_auto_20210510_1411'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'Location tag',
                'verbose_name_plural': 'Location tags',
            },
        ),
        migrations.CreateModel(
            name='TaggedLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='service.service')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_locations', to='service.locationtag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='service',
            name='locationTags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='service.TaggedLocation', to='service.LocationTag', verbose_name='Tags'),
        ),
    ]