# Generated by Django 4.2.2 on 2023-07-12 08:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('examapp', '0025_pupilanswer_is_in_action'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='subjects',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examapp.subject'),
        ),
    ]