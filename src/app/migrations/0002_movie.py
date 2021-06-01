# Generated by Django 3.2.3 on 2021-05-29 08:43

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название фильма')),
                ('description', models.TextField(verbose_name='Описание')),
                ('poster', models.ImageField(upload_to='', verbose_name='Главная картинка')),
                ('trailer', models.URLField(max_length=100, verbose_name='Ссылка на трейлер')),
                ('type', multiselectfield.db.fields.MultiSelectField(choices=[(0, '3D'), (1, '2D'), (2, 'IMAX')], max_length=5, verbose_name='Тип кино')),
                ('duration', models.DurationField(null=True, verbose_name='Продолжительность')),
                ('is_active', models.BooleanField(default=False, verbose_name='В прокате?')),
                ('release_date', models.DateField(verbose_name='Дата выхода')),
                ('seo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.seoparameters', verbose_name='SEO блок')),
            ],
        ),
    ]