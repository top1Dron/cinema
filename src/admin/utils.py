import logging

from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from admin.forms import MainBannerForm, Gallery, NewsAndStockBannerForm
from app.models import MainPageBanner, NewsAndStockBanner, Image


logger = logging.getLogger(__name__)


def get_main_page_obj():
    return MainPageBanner.objects.first()


def get_news_and_stock_obj():
    return NewsAndStockBanner.objects.first()


def get_forms_in_banner_page(post_dict=None, files_dict=None, method:str='GET') -> tuple:

    main_page_obj = get_main_page_obj()
    if main_page_obj is not None:
        return update_banner_form(main_page_obj, post_dict, files_dict, method)
    else:
        return create_banner_page(post_dict, files_dict, method)


def create_banner_page(post_dict, files_dict, method):
    redirect_available = False
    main_form = MainBannerForm()
    main_gallery = Gallery(queryset=Image.objects.none())
    if method == 'POST':
        main_form = MainBannerForm(post_dict, files_dict)
        if main_form.is_valid():
            main = main_form.save(commit=False)
            main_gallery = Gallery(post_dict, files_dict, instance=main)
            logger.info(main_gallery.is_valid())
            if main_gallery.is_valid():
                main.save()
                main_gallery.save()
                redirect_available = True
    return main_form, main_gallery, redirect_available


def update_banner_form(main_page_obj, post_dict, files_dict, method):
    redirect_available = False
    main_form = MainBannerForm(instance=main_page_obj)
    extra_count = 4 - main_page_obj.gallery.all().count() % 4
    extra_count = 0 if extra_count == 4 and main_page_obj.gallery.all().count() > 0 else extra_count
    UpdateGallery = generic_inlineformset_factory(Image, can_delete=True,
        extra=extra_count)
    main_gallery = UpdateGallery(post_dict or None, files_dict or None, queryset=main_page_obj.gallery.all(), instance=main_page_obj)

    if method == 'POST':
        main_form = MainBannerForm(post_dict, files_dict, instance=main_page_obj)
        if (main_form.is_valid()and main_gallery.is_valid()):
            main_form.save()
            main_gallery.save()
            redirect_available = True

    return main_form, main_gallery, redirect_available


def get_forms_in_news_and_stocks_banner_page(post_dict=None, files_dict=None, method:str='GET') -> tuple:
    news_obj = get_news_and_stock_obj()
    if news_obj is not None:
        return update_news_banner_page(news_obj, post_dict, files_dict, method)
    else:
        return create_news_banner_page(post_dict, files_dict, method)


def create_news_banner_page(post_dict, files_dict, method):
    redirect_available = False
    form = NewsAndStockBannerForm()
    gallery = Gallery(queryset=Image.objects.none())
    if method == 'POST':
        form = NewsAndStockBannerForm(post_dict, files_dict)
        if form.is_valid():
            main = form.save(commit=False)
            gallery = Gallery(post_dict, files_dict, instance=main)
            logger.info(gallery.is_valid())
            if gallery.is_valid():
                main.save()
                gallery.save()
                redirect_available = True
    return form, gallery, redirect_available


def update_news_banner_page(news_obj, post_dict, files_dict, method):
    redirect_available = False
    form = NewsAndStockBannerForm(instance=news_obj)
    extra_count = 4 - news_obj.gallery.all().count() % 4
    extra_count = 0 if extra_count == 4 and news_obj.gallery.all().count() > 0 else extra_count
    UpdateGallery = generic_inlineformset_factory(Image, can_delete=True,
        extra=extra_count)
    gallery = UpdateGallery(post_dict or None, files_dict or None, queryset=news_obj.gallery.all(), instance=news_obj)

    if method == 'POST':
        form = NewsAndStockBannerForm(post_dict, files_dict, instance=news_obj)
        logger.info(gallery.is_valid())
        logger.info(gallery.errors)
        if (form.is_valid()and gallery.is_valid()):
            form.save()
            gallery.save()
            redirect_available = True

    return form, gallery, redirect_available
