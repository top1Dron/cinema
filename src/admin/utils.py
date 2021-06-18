import json
import logging
from users.models import User

from django.conf import settings
from django.contrib import messages
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _

from admin.forms import (AboutCinemaForm, AdvertiseForm, ChildrenRoomForm, 
    MainBannerForm, Gallery, MainPageForm, NewsAndStockBannerForm, 
    SeoParametersForm, CafeBarForm, VipHallForm, MobileAppForm, MailingForm)
from admin.models import Mail
from app.models import (MainPage, MainPageBanner, NewsAndStockBanner, 
    Image, CafeBarPage, VipHallPage, AboutCinemaPage, AdvertisePage,
    ChildrenRoomPage, MobileAppPage, HallPlace, Hall)


logger = logging.getLogger(__name__)


def make_mailing(request):
    if request.POST.get('recipients') == '0':
        users = [u.email for u in User.objects.exclude(is_staff=True, is_superuser=True)]
    else:
        users = request.POST.get('users').split(',')
    file_id = request.POST.get('file_id')
    subject = request.POST.get('subject')
    message = ''
    if users[0] == '' or not file_id or not subject:
        if users[0] == '':
            messages.error(request, _('Выберите хоть одного получателя письма'))
        if not file_id:
            messages.error(request, _('Загрузите email или выберите из существующих'))
        if not subject:
            messages.error(request, _('Перед отправкой сообщения укажите его заголовок'))
        return None
    if file_id == 'new':
        form = MailingForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save()
            message = strip_tags(render_to_string(file.email.url.removeprefix('/media/emails/')))
    else:
        mail = get_object_or_404(Mail, pk=file_id)
        message = strip_tags(render_to_string(mail.email.url.removeprefix('/media/emails/')))
    send_email(subject, message, users)


def send_email(subject:str, message:str, to:list):
    '''
    function for send email
    '''
    send_mail(
        subject, 
        message, 
        settings.EMAIL_HOST_USER, 
        to,
        fail_silently=False,
    )


def get_main_page_banner_obj():
    return MainPageBanner.objects.first()


def get_news_and_stock_obj():
    return NewsAndStockBanner.objects.first()


def get_main_page_obj():
    return MainPage.objects.first()


def get_cafe_bar_page_obj():
    return CafeBarPage.objects.first()


def get_vip_hall_page_obj():
    return VipHallPage.objects.first()


def get_about_cinema_page_obj():
    return AboutCinemaPage.objects.first()


def get_advertise_page_obj():
    return AdvertisePage.objects.first()


def get_children_room_page_obj():
    return ChildrenRoomPage.objects.first()


def get_mobile_app_page_obj():
    return MobileAppPage.objects.first()


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
        form = CafeBarForm(post_dict, files_dict)
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
        form = CafeBarForm(post_dict, files_dict, instance=cafebar)
        seo_form = SeoParametersForm(post_dict, instance=cafebar.seo)
        if form.is_valid() and seo_form.is_valid() and gallery.is_valid():
            cafebar = form.save(commit=False)
            cafebar.seo = seo_form.save()
            cafebar.save()
            gallery.save()
            redirect_available = True
    return form, gallery, seo_form, redirect_available


def get_forms_in_vip_hall_page(post_dict:dict, files_dict:dict, method:str) -> tuple:
    viphall = get_vip_hall_page_obj()
    if viphall is not None:
        return update_vip_hall_page(viphall, post_dict, files_dict, method)
    else:
        return create_vip_hall_page(post_dict, files_dict, method)


def create_vip_hall_page(post_dict, files_dict, method):
    redirect_available = False
    form = VipHallForm()
    seo_form = SeoParametersForm()
    gallery = Gallery(queryset=Image.objects.none(), prefix='vip_hall_page')
    if method == 'POST':
        form = VipHallForm(post_dict, files_dict)
        seo_form = SeoParametersForm(post_dict)
        if form.is_valid() and seo_form.is_valid():
            viphall = form.save(commit=False)
            gallery = Gallery(post_dict, files_dict, instance=viphall, prefix='vip_hall_page')
            if gallery.is_valid():
                viphall.seo = seo_form.save()
                viphall.save()
                gallery.save()
                redirect_available = True
    return form, gallery, seo_form, redirect_available


def update_vip_hall_page(viphall, post_dict, files_dict, method):
    redirect_available = False
    form = VipHallForm(instance=viphall)
    seo_form = SeoParametersForm(instance=viphall.seo)
    extra_count = 4 - viphall.gallery.all().count() % 4
    extra_count = 0 if extra_count == 4 and viphall.gallery.all().count() > 0 else extra_count
    UpdateGallery = generic_inlineformset_factory(Image, can_delete=True,
        extra=extra_count)
    gallery = UpdateGallery(post_dict or None, files_dict or None, queryset=viphall.gallery.all(), instance=viphall, prefix='vip_hall_page')
    if method == 'POST':
        form = VipHallForm(post_dict, files_dict, instance=viphall)
        seo_form = SeoParametersForm(post_dict, instance=viphall.seo)
        if form.is_valid() and seo_form.is_valid() and gallery.is_valid():
            viphall = form.save(commit=False)
            viphall.seo = seo_form.save()
            viphall.save()
            gallery.save()
            redirect_available = True
    return form, gallery, seo_form, redirect_available


def get_forms_in_about_cinema_page(post_dict:dict, files_dict:dict, method:str) -> tuple:
    cinema = get_about_cinema_page_obj()
    if cinema is not None:
        return update_about_cinema_page(cinema, post_dict, files_dict, method)
    else:
        return create_about_cinema_page(post_dict, files_dict, method)


def create_about_cinema_page(post_dict, files_dict, method):
    redirect_available = False
    form = AboutCinemaForm()
    seo_form = SeoParametersForm()
    gallery = Gallery(queryset=Image.objects.none(), prefix='about_cinema_page')
    if method == 'POST':
        form = AboutCinemaForm(post_dict, files_dict)
        seo_form = SeoParametersForm(post_dict)
        if form.is_valid() and seo_form.is_valid():
            cinema = form.save(commit=False)
            gallery = Gallery(post_dict, files_dict, instance=cinema, prefix='about_cinema_page')
            if gallery.is_valid():
                cinema.seo = seo_form.save()
                cinema.save()
                gallery.save()
                redirect_available = True
    return form, gallery, seo_form, redirect_available


def update_about_cinema_page(cinema, post_dict, files_dict, method):
    redirect_available = False
    form = AboutCinemaForm(instance=cinema)
    seo_form = SeoParametersForm(instance=cinema.seo)
    extra_count = 4 - cinema.gallery.all().count() % 4
    extra_count = 0 if extra_count == 4 and cinema.gallery.all().count() > 0 else extra_count
    UpdateGallery = generic_inlineformset_factory(Image, can_delete=True,
        extra=extra_count)
    gallery = UpdateGallery(post_dict or None, files_dict or None, queryset=cinema.gallery.all(), instance=cinema, prefix='about_cinema_page')
    if method == 'POST':
        form = AboutCinemaForm(post_dict, files_dict, instance=cinema)
        seo_form = SeoParametersForm(post_dict, instance=cinema.seo)
        if form.is_valid() and seo_form.is_valid() and gallery.is_valid():
            cinema = form.save(commit=False)
            cinema.seo = seo_form.save()
            cinema.save()
            gallery.save()
            redirect_available = True
    return form, gallery, seo_form, redirect_available


def get_forms_in_advertise_page(post_dict:dict, files_dict:dict, method:str) -> tuple:
    advertise = get_advertise_page_obj()
    if advertise is not None:
        return update_advertise_page(advertise, post_dict, files_dict, method)
    else:
        return create_advertise_page(post_dict, files_dict, method)


def create_advertise_page(post_dict, files_dict, method):
    redirect_available = False
    form = AdvertiseForm()
    seo_form = SeoParametersForm()
    gallery = Gallery(queryset=Image.objects.none(), prefix='advertise_page')
    if method == 'POST':
        form = AdvertiseForm(post_dict, files_dict)
        seo_form = SeoParametersForm(post_dict)
        if form.is_valid() and seo_form.is_valid():
            advertise = form.save(commit=False)
            gallery = Gallery(post_dict, files_dict, instance=advertise, prefix='advertise_page')
            if gallery.is_valid():
                advertise.seo = seo_form.save()
                advertise.save()
                gallery.save()
                redirect_available = True
    return form, gallery, seo_form, redirect_available


def update_advertise_page(advertise, post_dict, files_dict, method):
    redirect_available = False
    form = AdvertiseForm(instance=advertise)
    seo_form = SeoParametersForm(instance=advertise.seo)
    extra_count = 4 - advertise.gallery.all().count() % 4
    extra_count = 0 if extra_count == 4 and advertise.gallery.all().count() > 0 else extra_count
    UpdateGallery = generic_inlineformset_factory(Image, can_delete=True,
        extra=extra_count)
    gallery = UpdateGallery(post_dict or None, files_dict or None, queryset=advertise.gallery.all(), instance=advertise, prefix='advertise_page')
    if method == 'POST':
        form = AdvertiseForm(post_dict, files_dict, instance=advertise)
        seo_form = SeoParametersForm(post_dict, instance=advertise.seo)
        if form.is_valid() and seo_form.is_valid() and gallery.is_valid():
            advertise = form.save(commit=False)
            advertise.seo = seo_form.save()
            advertise.save()
            gallery.save()
            redirect_available = True
    return form, gallery, seo_form, redirect_available


def get_forms_in_children_room_page(post_dict:dict, files_dict:dict, method:str) -> tuple:
    children_room = get_children_room_page_obj()
    if children_room is not None:
        return update_children_room_page(children_room, post_dict, files_dict, method)
    else:
        return create_children_room_page(post_dict, files_dict, method)


def create_children_room_page(post_dict, files_dict, method):
    redirect_available = False
    form = ChildrenRoomForm()
    seo_form = SeoParametersForm()
    gallery = Gallery(queryset=Image.objects.none(), prefix='children_room_page')
    if method == 'POST':
        form = ChildrenRoomForm(post_dict, files_dict)
        seo_form = SeoParametersForm(post_dict)
        if form.is_valid() and seo_form.is_valid():
            children_room = form.save(commit=False)
            gallery = Gallery(post_dict, files_dict, instance=children_room, prefix='children_room_page')
            if gallery.is_valid():
                children_room.seo = seo_form.save()
                children_room.save()
                gallery.save()
                redirect_available = True
    return form, gallery, seo_form, redirect_available


def update_children_room_page(children_room, post_dict, files_dict, method):
    redirect_available = False
    form = ChildrenRoomForm(instance=children_room)
    seo_form = SeoParametersForm(instance=children_room.seo)
    extra_count = 4 - children_room.gallery.all().count() % 4
    extra_count = 0 if extra_count == 4 and children_room.gallery.all().count() > 0 else extra_count
    UpdateGallery = generic_inlineformset_factory(Image, can_delete=True,
        extra=extra_count)
    gallery = UpdateGallery(post_dict or None, files_dict or None, queryset=children_room.gallery.all(), instance=children_room, prefix='children_room_page')
    if method == 'POST':
        form = ChildrenRoomForm(post_dict, files_dict, instance=children_room)
        seo_form = SeoParametersForm(post_dict, instance=children_room.seo)
        if form.is_valid() and seo_form.is_valid() and gallery.is_valid():
            children_room = form.save(commit=False)
            children_room.seo = seo_form.save()
            children_room.save()
            gallery.save()
            redirect_available = True
    return form, gallery, seo_form, redirect_available


def get_forms_in_mobile_app_page(post_dict:dict, files_dict:dict, method:str) -> tuple:
    mobile_app = get_mobile_app_page_obj()
    if mobile_app is not None:
        return update_mobile_app_page(mobile_app, post_dict, files_dict, method)
    else:
        return create_mobile_app_page(post_dict, files_dict, method)


def create_mobile_app_page(post_dict, files_dict, method):
    redirect_available = False
    form = MobileAppForm()
    seo_form = SeoParametersForm()
    gallery = Gallery(queryset=Image.objects.none(), prefix='mobile_app_page')
    if method == 'POST':
        form = MobileAppForm(post_dict, files_dict)
        seo_form = SeoParametersForm(post_dict)
        if form.is_valid() and seo_form.is_valid():
            mobile_app = form.save(commit=False)
            gallery = Gallery(post_dict, files_dict, instance=mobile_app, prefix='mobile_app_page')
            if gallery.is_valid():
                mobile_app.seo = seo_form.save()
                mobile_app.save()
                gallery.save()
                redirect_available = True
    return form, gallery, seo_form, redirect_available


def update_mobile_app_page(mobile_app, post_dict, files_dict, method):
    redirect_available = False
    form = MobileAppForm(instance=mobile_app)
    seo_form = SeoParametersForm(instance=mobile_app.seo)
    extra_count = 4 - mobile_app.gallery.all().count() % 4
    extra_count = 0 if extra_count == 4 and mobile_app.gallery.all().count() > 0 else extra_count
    UpdateGallery = generic_inlineformset_factory(Image, can_delete=True,
        extra=extra_count)
    gallery = UpdateGallery(post_dict or None, files_dict or None, queryset=mobile_app.gallery.all(), instance=mobile_app, prefix='mobile_app_page')
    if method == 'POST':
        form = MobileAppForm(post_dict, files_dict, instance=mobile_app)
        seo_form = SeoParametersForm(post_dict, instance=mobile_app.seo)
        if form.is_valid() and seo_form.is_valid() and gallery.is_valid():
            mobile_app = form.save(commit=False)
            mobile_app.seo = seo_form.save()
            mobile_app.save()
            gallery.save()
            redirect_available = True
    return form, gallery, seo_form, redirect_available


def save_hall_places(json_scheme, hall):
    scheme = json.loads(json_scheme)
    for key, value in scheme.items():
        HallPlace.objects.create(hall=hall,
            real_row=value['real_row'],
            row=-1 if value['row'] == ' ' else value['row'],
            real_position=value['real_pos'],
            number=-1 if value['number'] == ' ' else value['number'],
            is_vip=value['vip'],
        )


def update_hall_places(json_scheme, hall):
    hall.places.all().delete()
    save_hall_places(json_scheme, hall)