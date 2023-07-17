# Generated by Django 4.2.2 on 2023-07-12 23:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examapp', '0029_result_questions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examforgroup',
            name='ended_users',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='result',
            name='answers',
            field=models.ManyToManyField(blank=True, to='examapp.pupilanswer'),
        ),
        migrations.AlterField(
            model_name='result',
            name='questions',
            field=models.ManyToManyField(blank=True, to='examapp.question'),
        ),
    ]
