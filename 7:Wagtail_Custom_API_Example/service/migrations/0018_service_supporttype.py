# Generated by Django 3.1.8 on 2021-04-22 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0017_remove_service_supporttype'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='supportType',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
