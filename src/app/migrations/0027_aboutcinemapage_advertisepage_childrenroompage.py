# Generated by Django 3.2.3 on 2021-06-11 10:34

import app.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_auto_20210611_1303'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChildrenRoomPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('title_ru', models.CharField(max_length=50, null=True)),
                ('title_uk', models.CharField(max_length=50, null=True)),
                ('description', models.TextField()),
                ('description_ru', models.TextField(null=True)),
                ('description_uk', models.TextField(null=True)),
                ('main_image', models.ImageField(blank=True, null=True, upload_to=app.models.get_upload_path, verbose_name='Главная картинка')),
                ('seo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.seoparameters', verbose_name='SEO блок')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AdvertisePage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('title_ru', models.CharField(max_length=50, null=True)),
                ('title_uk', models.CharField(max_length=50, null=True)),
                ('description', models.TextField()),
                ('description_ru', models.TextField(null=True)),
                ('description_uk', models.TextField(null=True)),
                ('main_image', models.ImageField(blank=True, null=True, upload_to=app.models.get_upload_path, verbose_name='Главная картинка')),
                ('seo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.seoparameters', verbose_name='SEO блок')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AboutCinemaPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('title_ru', models.CharField(max_length=50, null=True)),
                ('title_uk', models.CharField(max_length=50, null=True)),
                ('description', models.TextField()),
                ('description_ru', models.TextField(null=True)),
                ('description_uk', models.TextField(null=True)),
                ('main_image', models.ImageField(blank=True, null=True, upload_to=app.models.get_upload_path, verbose_name='Главная картинка')),
                ('seo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.seoparameters', verbose_name='SEO блок')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
