# Generated by Django 4.2.2 on 2023-07-12 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examapp', '0024_rename_answer_pupilanswer_answers'),
    ]

    operations = [
        migrations.AddField(
            model_name='pupilanswer',
            name='is_in_action',
            field=models.BooleanField(default=True),
        ),
    ]
