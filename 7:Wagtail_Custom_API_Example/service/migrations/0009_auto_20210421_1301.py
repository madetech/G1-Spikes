# Generated by Django 3.1.8 on 2021-04-21 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0008_auto_20210421_1300'),
    ]

    operations = [
        migrations.RenameField(
            model_name='servicepage',
            old_name='url',
            new_name='serviceUrl',
        ),
    ]
