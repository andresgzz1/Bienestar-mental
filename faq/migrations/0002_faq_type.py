# Generated by Django 3.2.16 on 2022-11-16 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='type',
            field=models.CharField(default=-2022, max_length=15, verbose_name='tipo'),
            preserve_default=False,
        ),
    ]
