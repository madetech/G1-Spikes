# Generated by Django 3.1.8 on 2021-04-22 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0016_auto_20210422_0935'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='supportType',
        ),
    ]
