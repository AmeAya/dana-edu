# Generated by Django 4.2.2 on 2023-07-27 00:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('examapp', '0033_alter_school_area'),
    ]

    operations = [
        migrations.RenameField(
            model_name='area',
            old_name='Region',
            new_name='region',
        ),
    ]