# Generated by Django 3.2.3 on 2021-06-21 18:32

import app.models
import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import multiselectfield.db.fields


class Migration(migrations.Migration):

    replaces = [('app', '0001_initial'), ('app', '0002_movie'), ('app', '0003_auto_20210529_2044'), ('app', '0004_auto_20210529_2139'), ('app', '0005_auto_20210530_1322'), ('app', '0006_auto_20210530_1411'), ('app', '0007_auto_20210601_1855'), ('app', '0008_auto_20210601_2134'), ('app', '0009_auto_20210601_2232'), ('app', '0010_auto_20210602_0040'), ('app', '0011_auto_20210602_0108'), ('app', '0012_banner'), ('app', '0013_auto_20210607_1407'), ('app', '0014_alter_bannerpage_rotational_speed'), ('app', '0015_auto_20210607_1519'), ('app', '0016_auto_20210607_1807'), ('app', '0017_auto_20210608_1228'), ('app', '0018_mainpage'), ('app', '0019_alter_mainpage_seo_text'), ('app', '0020_cafebarpage'), ('app', '0021_image_url'), ('app', '0022_alter_image_url'), ('app', '0023_auto_20210611_1024'), ('app', '0024_auto_20210611_1148'), ('app', '0025_viphallpage'), ('app', '0026_auto_20210611_1303'), ('app', '0027_aboutcinemapage_advertisepage_childrenroompage'), ('app', '0028_mobileapppage'), ('app', '0029_auto_20210614_1854'), ('app', '0030_hallplace'), ('app', '0031_auto_20210618_1431'), ('app', '0032_alter_hallplace_hall'), ('app', '0033_cinemacontactspage'), ('app', '0034_alter_cinemacontactspage_cinema'), ('app', '0035_auto_20210619_0108'), ('app', '0036_alter_movie_genre'), ('app', '0037_auto_20210619_0154'), ('app', '0038_session'), ('app', '0039_alter_session_format'), ('app', '0040_ticket'), ('app', '0041_auto_20210620_1956')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeoParameters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seo_url', models.URLField(blank=True, null=True)),
                ('seo_title', models.CharField(blank=True, max_length=50, null=True)),
                ('seo_keywords', models.CharField(blank=True, max_length=50, null=True)),
                ('seo_description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cinema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='???????????????? ????????????????????')),
                ('description', models.TextField(verbose_name='????????????????')),
                ('condition', models.TextField(verbose_name='??????????????')),
                ('logo', models.ImageField(upload_to=app.models.get_upload_path, verbose_name='??????????????')),
                ('banner', models.ImageField(upload_to=app.models.get_upload_path, verbose_name='???????? ???????????????? ??????????????')),
                ('seo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.seoparameters', verbose_name='SEO ????????')),
                ('condition_ru', models.TextField(null=True, verbose_name='??????????????')),
                ('condition_uk', models.TextField(null=True, verbose_name='??????????????')),
                ('description_ru', models.TextField(null=True, verbose_name='????????????????')),
                ('description_uk', models.TextField(null=True, verbose_name='????????????????')),
                ('name_ru', models.CharField(max_length=50, null=True, unique=True, verbose_name='???????????????? ????????????????????')),
                ('name_uk', models.CharField(max_length=50, null=True, unique=True, verbose_name='???????????????? ????????????????????')),
            ],
            options={
                'unique_together': {('name', 'description', 'condition')},
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=app.models.get_upload_path)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('url', models.URLField(blank=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='Hall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=5, verbose_name='?????????? ????????')),
                ('description', models.TextField(verbose_name='????????????????')),
                ('banner', models.ImageField(upload_to=app.models.get_upload_path, verbose_name='?????????????? ????????????')),
                ('cinema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.cinema')),
                ('seo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.seoparameters', verbose_name='SEO ????????')),
                ('description_ru', models.TextField(null=True, verbose_name='????????????????')),
                ('description_uk', models.TextField(null=True, verbose_name='????????????????')),
                ('created', models.DateField(auto_now_add=True, default=datetime.datetime(2021, 6, 14, 15, 54, 24, 598967, tzinfo=utc), verbose_name='???????? ????????????????')),
                ('supported_types', multiselectfield.db.fields.MultiSelectField(choices=[(0, '3D'), (1, '2D'), (2, 'IMAX')], default=1, max_length=5, verbose_name='???????????????????????????? ??????????????')),
            ],
            options={
                'unique_together': {('number', 'cinema')},
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='???????????????? ????????????')),
                ('description', models.TextField(verbose_name='????????????????')),
                ('poster', models.ImageField(upload_to=app.models.get_upload_path, verbose_name='?????????????? ????????????????')),
                ('trailer', models.URLField(max_length=100, verbose_name='???????????? ???? ??????????????')),
                ('type', multiselectfield.db.fields.MultiSelectField(choices=[(0, '3D'), (1, '2D'), (2, 'IMAX')], max_length=5, verbose_name='?????? ????????')),
                ('duration', models.DurationField(null=True, verbose_name='??????????????????????????????????')),
                ('is_active', models.BooleanField(default=False, verbose_name='?? ???????????????')),
                ('release_date', models.DateField(verbose_name='???????? ????????????')),
                ('seo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.seoparameters', verbose_name='SEO ????????')),
                ('description_ru', models.TextField(null=True, verbose_name='????????????????')),
                ('description_uk', models.TextField(null=True, verbose_name='????????????????')),
                ('name_ru', models.CharField(max_length=100, null=True, verbose_name='???????????????? ????????????')),
                ('name_uk', models.CharField(max_length=100, null=True, verbose_name='???????????????? ????????????')),
                ('age_limit', models.CharField(blank=True, max_length=20, null=True, verbose_name='???????????????????? ??????????????????????')),
                ('budget', models.CharField(blank=True, max_length=100, null=True, verbose_name='????????????')),
                ('country', models.CharField(blank=True, max_length=50, null=True, verbose_name='????????????')),
                ('director', models.CharField(blank=True, max_length=250, null=True, verbose_name='????????????????')),
                ('genre', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('0', '??????????'), ('1', '???????????????????????????? ??????????'), ('2', '????????????'), ('3', '??????????????'), ('4', '?????????????? ??????????'), ('5', '???????????????????????????? ??????????'), ('6', '??????????'), ('7', '???????????????????????? ??????????'), ('8', '??????????????'), ('9', '???????????????????????????????? ??????????'), ('10', '????????????????'), ('11', '??????????????????'), ('12', '??????????????'), ('13', '?????????????????????? ??????????'), ('14', '????????????????????'), ('15', '????????????'), ('16', '????????????-??????????????????????????'), ('17', '????????'), ('18', '??????????????????????'), ('19', '???????????????? ??????????'), ('20', '???????????????????? ??????????'), ('21', '????-??????'), ('22', '??????????????'), ('23', '??????????'), ('24', '??????????????')], max_length=100, null=True)),
                ('language', models.CharField(default='????????????????????', max_length=250, verbose_name='????????')),
                ('scriptwriter', models.CharField(blank=True, max_length=250, null=True, verbose_name='??????????????????')),
                ('age_limit_ru', models.CharField(blank=True, max_length=20, null=True, verbose_name='???????????????????? ??????????????????????')),
                ('age_limit_uk', models.CharField(blank=True, max_length=20, null=True, verbose_name='???????????????????? ??????????????????????')),
                ('budget_ru', models.CharField(blank=True, max_length=100, null=True, verbose_name='????????????')),
                ('budget_uk', models.CharField(blank=True, max_length=100, null=True, verbose_name='????????????')),
                ('country_ru', models.CharField(blank=True, max_length=50, null=True, verbose_name='????????????')),
                ('country_uk', models.CharField(blank=True, max_length=50, null=True, verbose_name='????????????')),
                ('director_ru', models.CharField(blank=True, max_length=250, null=True, verbose_name='????????????????')),
                ('director_uk', models.CharField(blank=True, max_length=250, null=True, verbose_name='????????????????')),
                ('language_ru', models.CharField(default='????????????????????', max_length=250, null=True, verbose_name='????????')),
                ('language_uk', models.CharField(default='????????????????????', max_length=250, null=True, verbose_name='????????')),
                ('scriptwriter_ru', models.CharField(blank=True, max_length=250, null=True, verbose_name='??????????????????')),
                ('scriptwriter_uk', models.CharField(blank=True, max_length=250, null=True, verbose_name='??????????????????')),
            ],
            options={
                'unique_together': {('name', 'description', 'release_date')},
                'ordering': ('-release_date',),
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='???????????????? ??????????????')),
                ('description', models.TextField(verbose_name='????????????????')),
                ('published', models.DateTimeField(auto_now_add=True, verbose_name='???????? ????????????????????')),
                ('main_image', models.ImageField(blank=True, null=True, upload_to=app.models.get_upload_path, verbose_name='?????????????? ????????????????')),
                ('youtube_link', models.URLField(blank=True, max_length=100, null=True, verbose_name='???????????? ???? ??????????')),
                ('seo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.seoparameters', verbose_name='SEO ????????')),
                ('description_ru', models.TextField(null=True, verbose_name='????????????????')),
                ('description_uk', models.TextField(null=True, verbose_name='????????????????')),
                ('title_ru', models.CharField(max_length=50, null=True, verbose_name='???????????????? ??????????????')),
                ('title_uk', models.CharField(max_length=50, null=True, verbose_name='???????????????? ??????????????')),
                ('status', models.BooleanField(default=False, verbose_name='????????????')),
            ],
            options={
                'unique_together': {('title', 'published')},
                'ordering': ('-published',),
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='???????????????? ??????????')),
                ('description', models.TextField(verbose_name='????????????????')),
                ('published', models.DateTimeField(auto_now_add=True, verbose_name='???????? ????????????????????')),
                ('main_image', models.ImageField(blank=True, null=True, upload_to=app.models.get_upload_path, verbose_name='?????????????? ????????????????')),
                ('youtube_link', models.URLField(blank=True, max_length=100, null=True, verbose_name='???????????? ???? ??????????')),
                ('seo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.seoparameters', verbose_name='SEO ????????')),
                ('description_ru', models.TextField(null=True, verbose_name='????????????????')),
                ('description_uk', models.TextField(null=True, verbose_name='????????????????')),
                ('title_ru', models.CharField(max_length=50, null=True, verbose_name='???????????????? ??????????')),
                ('title_uk', models.CharField(max_length=50, null=True, verbose_name='???????????????? ??????????')),
                ('status', models.BooleanField(default=False, verbose_name='????????????')),
            ],
            options={
                'unique_together': {('title', 'published')},
                'ordering': ('-published',),
            },
        ),
        migrations.CreateModel(
            name='MainPageBanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rotational_speed', models.CharField(choices=[('1', '1c'), ('2', '2c'), ('3', '3c'), ('4', '4c'), ('5', '5c'), ('6', '6c'), ('7', '7c'), ('8', '8c'), ('9', '9c')], max_length=5, verbose_name='???????????????? ????????????????')),
                ('backgroung_image', models.ImageField(upload_to=app.models.get_upload_path)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NewsAndStockBanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rotational_speed', models.CharField(choices=[('1', '1c'), ('2', '2c'), ('3', '3c'), ('4', '4c'), ('5', '5c'), ('6', '6c'), ('7', '7c'), ('8', '8c'), ('9', '9c')], max_length=5, verbose_name='???????????????? ????????????????')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MainPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number1', models.CharField(max_length=13, unique=True, validators=[django.core.validators.RegexValidator(regex='^(?:\\+38)?(?:\\(0[0-9][0-9]\\)[ .-]?[0-9]{3}[ .-]?[0-9]{2}[ .-]?[0-9]{2}|044[ .-]?[0-9]{3}[ .-]?[0-9]{2}[ .-]?[0-9]{2}|0[0-9][0-9][0-9]{7})$')])),
                ('number2', models.CharField(max_length=13, unique=True, validators=[django.core.validators.RegexValidator(regex='^(?:\\+38)?(?:\\(0[0-9][0-9]\\)[ .-]?[0-9]{3}[ .-]?[0-9]{2}[ .-]?[0-9]{2}|044[ .-]?[0-9]{3}[ .-]?[0-9]{2}[ .-]?[0-9]{2}|0[0-9][0-9][0-9]{7})$')])),
                ('seo_text', models.TextField(blank=True, null=True)),
                ('seo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.seoparameters', verbose_name='SEO ????????')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CafeBarPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('seo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.seoparameters', verbose_name='SEO ????????')),
                ('description_ru', models.TextField(null=True)),
                ('description_uk', models.TextField(null=True)),
                ('title_ru', models.CharField(max_length=50, null=True)),
                ('title_uk', models.CharField(max_length=50, null=True)),
                ('main_image', models.ImageField(blank=True, null=True, upload_to=app.models.get_upload_path, verbose_name='?????????????? ????????????????')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VipHallPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('title_ru', models.CharField(max_length=50, null=True)),
                ('title_uk', models.CharField(max_length=50, null=True)),
                ('description', models.TextField()),
                ('description_ru', models.TextField(null=True)),
                ('description_uk', models.TextField(null=True)),
                ('seo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.seoparameters', verbose_name='SEO ????????')),
                ('main_image', models.ImageField(blank=True, null=True, upload_to=app.models.get_upload_path, verbose_name='?????????????? ????????????????')),
            ],
            options={
                'abstract': False,
            },
        ),
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
                ('main_image', models.ImageField(blank=True, null=True, upload_to=app.models.get_upload_path, verbose_name='?????????????? ????????????????')),
                ('seo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.seoparameters', verbose_name='SEO ????????')),
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
                ('main_image', models.ImageField(blank=True, null=True, upload_to=app.models.get_upload_path, verbose_name='?????????????? ????????????????')),
                ('seo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.seoparameters', verbose_name='SEO ????????')),
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
                ('main_image', models.ImageField(blank=True, null=True, upload_to=app.models.get_upload_path, verbose_name='?????????????? ????????????????')),
                ('seo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.seoparameters', verbose_name='SEO ????????')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MobileAppPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('title_ru', models.CharField(max_length=50, null=True)),
                ('title_uk', models.CharField(max_length=50, null=True)),
                ('description', models.TextField()),
                ('description_ru', models.TextField(null=True)),
                ('description_uk', models.TextField(null=True)),
                ('main_image', models.ImageField(blank=True, null=True, upload_to=app.models.get_upload_path, verbose_name='?????????????? ????????????????')),
                ('seo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.seoparameters', verbose_name='SEO ????????')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HallPlace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row', models.IntegerField(verbose_name='??????')),
                ('real_position', models.PositiveIntegerField(verbose_name='???????????????? ???????????????????????????? ?? ????????')),
                ('number', models.IntegerField(verbose_name='??????????')),
                ('is_vip', models.BooleanField(default=False, verbose_name='VIP-???????????')),
                ('hall', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='places', to='app.hall')),
                ('real_row', models.PositiveIntegerField(default=-1, verbose_name='???????????????? ??????')),
            ],
            options={
                'unique_together': {('hall', 'row', 'real_position')},
            },
        ),
        migrations.CreateModel(
            name='CinemaContactsPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(blank=True, null=True)),
                ('coordinates', models.TextField(blank=True, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to=app.models.get_upload_path, verbose_name='??????????????')),
                ('cinema', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.cinema')),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(verbose_name='???????? ????????????')),
                ('format', models.IntegerField(choices=[(0, '3D'), (1, '2D'), (2, 'IMAX')], verbose_name='???????????? ????????????')),
                ('price', models.FloatField(verbose_name='???????? ???????????????? ????????????')),
                ('vip_price', models.FloatField(verbose_name='???????? VIP-????????????')),
                ('hall', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.hall')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.movie')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('0', 'C??????????????'), ('1', '????????????????????????'), ('2', '????????????')], default='0', max_length=1, verbose_name='C??????????')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.hallplace')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='app.session')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('session', 'place')},
            },
        ),
    ]
