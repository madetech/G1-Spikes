# Generated by Django 3.1.8 on 2021-04-21 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_auto_20210421_1256'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicepage',
            name='serviceName',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]