# Generated by Django 4.2.2 on 2023-07-09 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('examapp', '0016_result_currenttest'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CurrentTest',
            new_name='CurrentExam',
        ),
    ]
