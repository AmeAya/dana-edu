# Generated by Django 4.2.2 on 2023-07-12 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examapp', '0028_examforgroup_ended_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='questions',
            field=models.ManyToManyField(to='examapp.question'),
        ),
    ]
