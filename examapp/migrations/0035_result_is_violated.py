# Generated by Django 4.2.2 on 2023-08-16 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examapp', '0034_rename_region_area_region'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='is_violated',
            field=models.BooleanField(default=False),
        ),
    ]
