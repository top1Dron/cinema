# Generated by Django 3.2.3 on 2021-06-21 22:18

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial_squashed_0041_auto_20210620_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hall',
            name='created',
            field=models.DateField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='hall',
            name='supported_types',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(0, '3D'), (1, '2D'), (2, 'IMAX')], max_length=5, verbose_name='Поддерживаемые форматы'),
        ),
        migrations.AlterField(
            model_name='hallplace',
            name='real_row',
            field=models.PositiveIntegerField(verbose_name='Реальный ряд'),
        ),
    ]
