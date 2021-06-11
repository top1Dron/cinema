# Generated by Django 3.2.3 on 2021-06-07 11:07

import app.models
from django.db import migrations, models
import django_seconds_field


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_banner'),
    ]

    operations = [
        migrations.CreateModel(
            name='BannerPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rotational_speed', django_seconds_field.SecondsField(verbose_name='Скорость вращения')),
                ('backgroung_image', models.ImageField(upload_to=app.models.get_upload_path)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='Banner',
        ),
    ]