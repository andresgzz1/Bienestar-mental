# Generated by Django 3.2.16 on 2022-11-05 01:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0017_merge_20221104_1154'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='relaxation_techniques',
            name='state_professional',
        ),
    ]