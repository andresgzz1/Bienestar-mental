# Generated by Django 3.2.16 on 2022-11-01 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_is_client'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userstandard',
            options={'verbose_name': 'userStandard', 'verbose_name_plural': 'usersStandard'},
        ),
    ]
