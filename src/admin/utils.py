import logging

from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.db.models.fields import files
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from admin.forms import MainBannerForm, Gallery, MainPageForm, NewsAndStockBannerForm, SeoParametersForm, CafeBarForm
from app.models import MainPage, MainPageBanner, NewsAndStockBanner, Image, CafeBarPage


logger = logging.getLogger(__name__)


def get_main_page_banner_obj():
    return MainPageBanner.objects.first()


def get_news_and_stock_obj():
    return NewsAndStockBanner.objects.first()


def get_main_page_obj():
    return MainPage.objects.first()


def get_cafe_bar_page_obj():
    return CafeBarPage.objects.first()


def get_forms_in_banner_page(post_dict=None, files_dict=None, method:str='GET') -> tuple:

    main_page_obj = get_main_page_banner_obj()
    if main_page_obj is not None:
        return update_banner_form(main_page_obj, post_dict, files_dict, method)
    else:
        return create_banner_page(post_dict, files_dict, method)


def create_banner_page(post_dict, files_dict, method):
    redirect_available = False
    main_form = MainBannerForm()
    main_gallery = Gallery(queryset=Image.objects.none(), prefix="on_top_main")
    if method == 'POST':
        main_form = MainBannerForm(post_dict, files_dict)
        if main_form.is_valid():
            main = main_form.save(commit=False)
            main_gallery = Gallery(post_dict, files_dict, instance=main, prefix="on_top_main")
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
    main_gallery = UpdateGallery(post_dict or None, files_dict or None, 
        queryset=main_page_obj.gallery.all(), 
        instance=main_page_obj,
        prefix="on_top_main")

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
    gallery = Gallery(queryset=Image.objects.none(), prefix='news_and_stocks')
    if method == 'POST':
        form = NewsAndStockBannerForm(post_dict, files_dict)
        if form.is_valid():
            main = form.save(commit=False)
            gallery = Gallery(post_dict, files_dict, instance=main, prefix='news_and_stocks')
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
    gallery = UpdateGallery(post_dict or None, files_dict or None, queryset=news_obj.gallery.all(), instance=news_obj, prefix='news_and_stocks')

    if method == 'POST':
        form = NewsAndStockBannerForm(post_dict, files_dict, instance=news_obj)
        if (form.is_valid()and gallery.is_valid()):
            form.save()
            gallery.save()
            redirect_available = True

    return form, gallery, redirect_available


def get_forms_in_main_page(post_dict, method):
    main_page = get_main_page_obj()
    if main_page is not None:
        return update_main_page(main_page, post_dict, method)
    else:
        return create_main_page(post_dict, method)


def create_main_page(post_dict:dict, method:str):
    redirect_available = False
    form = MainPageForm()
    seo_form = SeoParametersForm()
    if method == 'POST':
        form = MainPageForm(post_dict)
        seo_form = SeoParametersForm(post_dict)
        if form.is_valid() and seo_form.is_valid():
            page = form.save(commit=False)
            page.seo = seo_form.save()
            page.save()
            redirect_available = True
    return form, seo_form, redirect_available

def update_main_page(page:MainPage, post_dict:dict, method:str):
    redirect_available = False
    form = MainPageForm(instance=page)
    seo_form = SeoParametersForm(instance=page.seo)
    if method == 'POST':
        form = MainPageForm(post_dict, instance=page)
        seo_form = SeoParametersForm(post_dict, instance=page.seo)
        if form.is_valid() and seo_form.is_valid():
            page = form.save(commit=False)
            page.seo = seo_form.save()
            page.save()
            redirect_available = True
    return form, seo_form, redirect_available


def get_forms_in_cafe_bar_pages(post_dict:dict, files_dict:dict, method:str) -> tuple:
    cafebar = get_cafe_bar_page_obj()
    if cafebar is not None:
        return update_cafe_bar_page(cafebar, post_dict, files_dict, method)
    else:
        return create_cafe_bar_page(post_dict, files_dict, method)


def create_cafe_bar_page(post_dict, files_dict, method):
    redirect_available = False
    form = CafeBarForm()
    seo_form = SeoParametersForm()
    gallery = Gallery(queryset=Image.objects.none(), prefix='cafe_bar_page')
    if method == 'POST':
        form = CafeBarForm(post_dict)
        seo_form = SeoParametersForm(post_dict)
        if form.is_valid() and seo_form.is_valid():
            cafebar = form.save(commit=False)
            gallery = Gallery(post_dict, files_dict, instance=cafebar, prefix='cafe_bar_page')
            if gallery.is_valid():
                cafebar.seo = seo_form.save()
                cafebar.save()
                gallery.save()
                redirect_available = True
    return form, gallery, seo_form, redirect_available


def update_cafe_bar_page(cafebar, post_dict, files_dict, method):
    redirect_available = False
    form = CafeBarForm(instance=cafebar)
    seo_form = SeoParametersForm(instance=cafebar.seo)
    extra_count = 4 - cafebar.gallery.all().count() % 4
    extra_count = 0 if extra_count == 4 and cafebar.gallery.all().count() > 0 else extra_count
    UpdateGallery = generic_inlineformset_factory(Image, can_delete=True,
        extra=extra_count)
    gallery = UpdateGallery(post_dict or None, files_dict or None, queryset=cafebar.gallery.all(), instance=cafebar, prefix='cafe_bar_page')
    if method == 'POST':
        form = MainPageForm(post_dict, instance=cafebar)
        seo_form = SeoParametersForm(post_dict, instance=cafebar.seo)
        if form.is_valid() and seo_form.is_valid() and gallery.is_valid():
            cafebar = form.save(commit=False)
            cafebar.seo = seo_form.save()
            cafebar.save()
            gallery.save()
            redirect_available = True
    return form, gallery, seo_form, redirect_available