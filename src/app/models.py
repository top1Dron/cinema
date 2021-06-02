from datetime import datetime as dt
from pathlib import Path
import os

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from multiselectfield import MultiSelectField


def get_upload_path(instance, filename):
    return Path('uploads') / dt.now().strftime('%Y/%m-%d') / filename


class Image(models.Model):
    image = models.ImageField(upload_to=get_upload_path)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class SeoParameters(models.Model):
    seo_url = models.URLField(max_length=200, null=True, blank=True)
    seo_title = models.CharField(max_length=50, null=True, blank=True)
    seo_keywords = models.CharField(max_length=50, null=True, blank=True)
    seo_description = models.TextField(null=True, blank=True)


class Movie(models.Model):
    MOVIE_TYPES = (
        (0, '3D'),
        (1, '2D'),
        (2, 'IMAX')
    )
    name = models.CharField(_('Название фильма'), max_length=100)
    description = models.TextField(_("Описание"))
    poster = models.ImageField(_("Главная картинка"), upload_to=get_upload_path)
    gallery = GenericRelation(Image, related_query_name='movie')
    trailer = models.URLField(_("Ссылка на трейлер"), max_length=100)
    type = MultiSelectField(choices=MOVIE_TYPES, verbose_name=_('Тип кино'))
    duration = models.DurationField(_("Продолжительность"), null=True)
    is_active = models.BooleanField(_("В прокате?"), default=False)
    release_date = models.DateField(_("Дата выхода"))
    seo = models.ForeignKey(SeoParameters, verbose_name=_("SEO блок"), on_delete=models.DO_NOTHING, null=True)

    class Meta:
        unique_together = ('name', 'description', 'release_date')
        ordering = ('-release_date', )

    def __str__(self):
        return f'{self.name} - {self.release_date}'
    
    

class Cinema(models.Model):
    name = models.CharField(_('Название кинотеатра'), max_length=50)
    description = models.TextField(_("Описание"))
    condition = models.TextField(_("Условия"))
    logo = models.ImageField(_('Логотип'), upload_to=get_upload_path)
    banner = models.ImageField(_('Фото верхнего баннера'), upload_to=get_upload_path)
    gallery = GenericRelation(Image, related_query_name='cinema')
    seo = models.ForeignKey(SeoParameters, verbose_name=_("SEO блок"), on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ('name', 'description', 'condition')


class Hall(models.Model):
    number = models.CharField(_("Номер зала"), max_length=5)
    description = models.TextField(_("Описание"))
    banner = models.ImageField(_('Верхний баннер'), upload_to=get_upload_path)
    gallery = GenericRelation(Image, related_query_name='hall')
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    seo = models.ForeignKey(SeoParameters, verbose_name=_("SEO блок"), on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ('number', 'cinema')


class News(models.Model):
    title = models.CharField(_('Название новости'), max_length=50)
    description = models.TextField(_("Описание"))
    published = models.DateTimeField(_("Дата публикации"), auto_now_add=True)
    main_image = models.ImageField(_('Главная картинка'), upload_to=get_upload_path, null=True, blank=True)
    gallery = GenericRelation(Image, related_query_name='news')
    youtube_link = models.URLField(_("Ссылка на видео"), max_length=100, null=True, blank=True)
    status = models.BooleanField(_("Статус"), default=False)
    seo = models.ForeignKey(SeoParameters, verbose_name=_("SEO блок"), on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ('title', 'published')
        ordering = ('-published', )


class Stock(models.Model):
    title = models.CharField(_('Название акции'), max_length=50)
    description = models.TextField(_("Описание"))
    published = models.DateTimeField(_("Дата публикации"), auto_now_add=True)
    main_image = models.ImageField(_('Главная картинка'), upload_to=get_upload_path)
    gallery = GenericRelation(Image, related_query_name='stock')
    youtube_link = models.URLField(_("Ссылка на видео"), max_length=100)
    status = models.BooleanField(_("Статус"), default=False)
    seo = models.ForeignKey(SeoParameters, verbose_name=_("SEO блок"), on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ('title', 'published')
        ordering = ('-published', )


image_attributes = ('image', 'poster', 'logo', 'banner', 'main_image')


@receiver(models.signals.post_delete, sender=Image)
@receiver(models.signals.post_delete, sender=Movie)
@receiver(models.signals.post_delete, sender=Cinema)
@receiver(models.signals.post_delete, sender=Hall)
@receiver(models.signals.post_delete, sender=News)
@receiver(models.signals.post_delete, sender=Stock)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding sender object is deleted.
    """
    for attribute in image_attributes:
        if hasattr(instance, attribute):
            attr = getattr(instance, attribute)
            if attr:
                try:
                    if os.path.isfile(attr.path):
                        os.remove(attr.path)
                except ValueError:
                    pass

@receiver(models.signals.pre_save, sender=Image)
@receiver(models.signals.pre_save, sender=Movie)
@receiver(models.signals.pre_save, sender=Cinema)
@receiver(models.signals.pre_save, sender=Hall)
@receiver(models.signals.pre_save, sender=News)
@receiver(models.signals.pre_save, sender=Stock)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding sender object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        sender_obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return False
    for attribute in image_attributes:
        if hasattr(sender_obj, attribute):
            old_file = getattr(sender_obj, attribute)
        if hasattr(instance, attribute):
            new_file = getattr(instance, attribute)

    if not old_file == new_file:
        try:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
        except ValueError as e:
            pass