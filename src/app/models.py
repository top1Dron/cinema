from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _
from multiselectfield import MultiSelectField


class Image(models.Model):
    image = models.ImageField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class SeoParameters(models.Model):
    url = models.URLField(max_length=200)
    title = models.CharField(max_length=50)
    keywords = models.CharField(max_length=50)
    description = models.TextField()


class Movie:
    MOVIE_TYPES = (
        (0, '3D'),
        (1, '2D'),
        (2, 'IMAX')
    )
    name = models.CharField(_('Название фильма'), max_length=100)
    description = models.TextField(_("Описание"))
    poster = models.ImageField(_("Главная картинка"))
    gallery = GenericRelation(Image)
    trailer = models.URLField(_("Ссылка на трейлер"), max_length=100)
    type = MultiSelectField(choices=MOVIE_TYPES, verbose_name=_('Тип кино'))
    duration = models.DurationField(_("Продолжительность"))
    is_active = models.BooleanField(_("В прокате?"), default=False)
    release_date = models.DateField(_("Дата выхода"))
    seo = models.ForeignKey(SeoParameters, verbose_name=_("SEO блок"), on_delete=models.DO_NOTHING)
    

class Cinema(models.Model):
    name = models.CharField(_('Название кинотеатра'), max_length=50)
    description = models.TextField(_("Описание"))
    condition = models.TextField(_("Условия"))
    logo = models.ImageField(_('Логотип'))
    banner = models.ImageField(_('Фото верхнего баннера'))
    gallery = GenericRelation(Image)
    seo = models.ForeignKey(SeoParameters, verbose_name=_("SEO блок"), on_delete=models.DO_NOTHING)


class Hall(models.Model):
    number = models.CharField(_("Номер зала"), max_length=5)
    description = models.TextField(_("Описание"))
    banner = models.ImageField(_('Верхний баннер'))
    gallery = GenericRelation(Image)
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    seo = models.ForeignKey(SeoParameters, verbose_name=_("SEO блок"), on_delete=models.DO_NOTHING)


class News(models.Model):
    title = models.CharField(_('Название новости'), max_length=50)
    description = models.TextField(_("Описание"))
    published = models.DateTimeField(_("Дата публикации"), auto_now_add=True)
    main_image = models.ImageField(_('Главная картинка'))
    gallery = GenericRelation(Image)
    youtube_link = models.URLField(_("Ссылка на видео"), max_length=100)
    seo = models.ForeignKey(SeoParameters, verbose_name=_("SEO блок"), on_delete=models.DO_NOTHING)


class Stock(models.Model):
    title = models.CharField(_('Название акции'), max_length=50)
    description = models.TextField(_("Описание"))
    published = models.DateTimeField(_("Дата публикации"), auto_now_add=True)
    main_image = models.ImageField(_('Главная картинка'))
    gallery = GenericRelation(Image)
    youtube_link = models.URLField(_("Ссылка на видео"), max_length=100)
    seo = models.ForeignKey(SeoParameters, verbose_name=_("SEO блок"), on_delete=models.DO_NOTHING)