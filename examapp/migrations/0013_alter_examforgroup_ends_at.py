# Generated by Django 4.2.2 on 2023-07-04 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examapp', '0012_examforgroup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examforgroup',
            name='ends_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
