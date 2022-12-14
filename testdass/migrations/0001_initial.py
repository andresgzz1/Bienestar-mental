# Generated by Django 3.2.16 on 2022-11-15 00:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import embed_video.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='recomendation1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_msg', models.CharField(blank=True, max_length=600, null=True, verbose_name='recomendation text')),
                ('level', models.CharField(blank=True, max_length=600, null=True, verbose_name='level')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creacion')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha actualizacion')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Fecha eliminacion')),
            ],
            options={
                'verbose_name': 'recomendacion',
                'verbose_name_plural': 'recomendacion',
            },
        ),
        migrations.CreateModel(
            name='test1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='name')),
                ('pretest_text', models.CharField(blank=True, max_length=400, null=True, verbose_name='pretest text')),
                ('introduction_text', models.CharField(blank=True, max_length=400, null=True, verbose_name='introduction text')),
                ('state_config', models.BooleanField(default=False, verbose_name='config')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creacion')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha actualizacion')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Fecha eliminacion')),
            ],
            options={
                'verbose_name': 'test',
                'verbose_name_plural': 'tests',
            },
        ),
        migrations.CreateModel(
            name='testregister1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField()),
                ('result_total', models.IntegerField(blank=True, null=True, verbose_name='result_total')),
                ('result_depresion', models.CharField(blank=True, max_length=200, null=True, verbose_name='depresion')),
                ('result_ansiedad', models.CharField(blank=True, max_length=200, null=True, verbose_name='ansiedad')),
                ('result_estres', models.CharField(blank=True, max_length=200, null=True, verbose_name='ansiedad')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creacion')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha actualizacion')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Fecha eliminacion')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testdass.test1')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'test',
                'verbose_name_plural': 'tests',
            },
        ),
        migrations.CreateModel(
            name='respuestas_user1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alternative', models.IntegerField(verbose_name={0, 1, 2, 3})),
                ('question_text', models.CharField(max_length=200, verbose_name='text')),
                ('question_type', models.CharField(max_length=100, verbose_name='type')),
                ('question_id', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creacion')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha actualizacion')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Fecha eliminacion')),
                ('testregister', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testdass.testregister1')),
            ],
            options={
                'verbose_name': 'alternative',
                'verbose_name_plural': 'alternative',
            },
        ),
        migrations.CreateModel(
            name='relaxation_techniques1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_msg', models.CharField(blank=True, max_length=600, null=True, verbose_name='text')),
                ('level', models.CharField(blank=True, max_length=600, null=True, verbose_name='level')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creacion')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha actualizacion')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Fecha eliminacion')),
                ('state_professional', models.BooleanField(default=False, verbose_name='state professional')),
                ('recomendation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testdass.recomendation1')),
            ],
            options={
                'verbose_name': 'tecnica de relajaci??n',
                'verbose_name_plural': 'tecnicas de relajaci??n',
            },
        ),
        migrations.CreateModel(
            name='question1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200, verbose_name='text')),
                ('question_type', models.CharField(max_length=100, verbose_name='type')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creacion')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha actualizacion')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Fecha eliminacion')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testdass.test1')),
            ],
            options={
                'verbose_name': 'question',
                'verbose_name_plural': 'questions',
            },
        ),
        migrations.CreateModel(
            name='link_techniques1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_title', models.CharField(blank=True, max_length=600, null=True, verbose_name='text title')),
                ('url', embed_video.fields.EmbedVideoField()),
                ('autor', models.CharField(blank=True, max_length=600, null=True, verbose_name='autor')),
                ('canal', models.CharField(blank=True, max_length=600, null=True, verbose_name='canal')),
                ('origen', models.CharField(blank=True, max_length=600, null=True, verbose_name='level')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creacion')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha actualizacion')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Fecha eliminacion')),
                ('relaxation_techniques', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testdass.relaxation_techniques1')),
            ],
            options={
                'verbose_name': 'url de tecnica',
                'verbose_name_plural': 'urls de tecnicas',
            },
        ),
        migrations.CreateModel(
            name='alternative1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alternative', models.IntegerField(verbose_name={0, 1, 2, 3})),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creacion')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha actualizacion')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Fecha eliminacion')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testdass.question1')),
            ],
            options={
                'verbose_name': 'alternative',
                'verbose_name_plural': 'alternative',
            },
        ),
    ]
