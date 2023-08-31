# Generated by Django 4.2.2 on 2023-08-28 22:07

from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import parler.models


class Migration(migrations.Migration):

    dependencies = [
        ('examapp', '0036_variant_language_alter_variant_exam_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variant',
            name='exam_type',
        ),
        migrations.RemoveField(
            model_name='variant',
            name='language',
        ),
        migrations.RemoveField(
            model_name='variant',
            name='name',
        ),
        migrations.CreateModel(
            name='VariantTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(max_length=100)),
                ('exam_type', models.CharField(choices=[('MODO', 'MODO'), ('ENT', 'ENT')], max_length=10)),
                ('language', models.CharField(choices=[('KAZ', 'KAZ'), ('RUS', 'RUS')], max_length=3)),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='examapp.variant')),
            ],
            options={
                'verbose_name': 'variant Translation',
                'db_table': 'examapp_variant_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatableModel, models.Model),
        ),
    ]