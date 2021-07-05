import logging
from PIL import Image

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.http import JsonResponse, response
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView

from app.models import Image, Movie, News, Session, Stock, Cinema, CinemaContactsPage, User
from admin.forms import (AdminMovieForm, AdminNewsForm, AdminStockForm, SeoParametersForm, 
    Gallery, UserUpdateForm, MailingForm, AdminCinemaForm, AdminHallForm, CinemaContactsPageForm,
    AdminSessionForm, UserCreateForm)
from admin.models import Mail
from admin.utils import (get_forms_in_banner_page, get_forms_in_news_and_stocks_banner_page, 
    get_forms_in_main_page, get_forms_in_cafe_bar_pages, get_forms_in_vip_hall_page,
    get_forms_in_about_cinema_page, get_forms_in_advertise_page, get_forms_in_children_room_page,
    get_forms_in_mobile_app_page, make_mailing, save_hall_places, update_hall_places, create_session)
from app import utils
from users.forms import LoginForm
from users.models import User
from users.utils import get_user_by_email


logger = logging.getLogger(__name__)

@staff_member_required(login_url=reverse_lazy('admin:login'))
def index(request):
    users_count = User.objects.all().count()
    men_count = User.objects.filter(gender='M').count()
    women_count = User.objects.filter(gender='W').count()
    month, sessions_count = utils.get_month_sessions()
    movie_fees = utils.get_movies_fees()
    return render(request, 'admin/statistics.html', {
        'users_count': users_count,
        'men_count': men_count,
        'women_count': women_count,
        'sessions_count': sessions_count,
        'month': month,
        'movie_fees': movie_fees,
    })


@staff_member_required(login_url=reverse_lazy('admin:login'))
def main_page(request):
    form, seo_form, redirect_available = get_forms_in_main_page(request.POST, request.method)

    if redirect_available:
        return redirect(reverse_lazy('admin:main_page'))
    else:
        return render(request, 'admin/main_page.html', {
            'form': form,
            'seo_form': seo_form,
        })


@staff_member_required(login_url=reverse_lazy('admin:login'))
def cafe_bar_page(request):
    form, gallery, seo_form, redirect_available = get_forms_in_cafe_bar_pages(request.POST, request.FILES, request.method)
    if redirect_available:
        return redirect(reverse_lazy('admin:cafe_bar_page'))
    else:
        return render(request, 'admin/cafe_bar_page.html', {
            'form': form,
            'seo_form': seo_form,
            'gallery': gallery
        })


@staff_member_required(login_url=reverse_lazy('admin:login'))
def vip_hall_page(request):
    form, gallery, seo_form, redirect_available = get_forms_in_vip_hall_page(request.POST, request.FILES, request.method)
    if redirect_available:
        return redirect(reverse_lazy('admin:vip_hall_page'))
    else:
        return render(request, 'admin/vip-hall-page.html', {
            'form': form,
            'seo_form': seo_form,
            'gallery': gallery
        })


@staff_member_required(login_url=reverse_lazy('admin:login'))
def about_cinema_page(request):
    form, gallery, seo_form, redirect_available = get_forms_in_about_cinema_page(request.POST, request.FILES, request.method)
    if redirect_available:
        return redirect(reverse_lazy('admin:about_cinema_page'))
    else:
        return render(request, 'admin/about-cinema-page.html', {
            'form': form,
            'seo_form': seo_form,
            'gallery': gallery
        })


@staff_member_required(login_url=reverse_lazy('admin:login'))
def advertise_page(request):
    form, gallery, seo_form, redirect_available = get_forms_in_advertise_page(request.POST, request.FILES, request.method)
    if redirect_available:
        return redirect(reverse_lazy('admin:advertise_page'))
    else:
        return render(request, 'admin/advertise-page.html', {
            'form': form,
            'seo_form': seo_form,
            'gallery': gallery
        })


@staff_member_required(login_url=reverse_lazy('admin:login'))
def children_room_page(request):
    form, gallery, seo_form, redirect_available = get_forms_in_children_room_page(request.POST, request.FILES, request.method)
    if redirect_available:
        return redirect(reverse_lazy('admin:children_room_page'))
    else:
        return render(request, 'admin/children-room-page.html', {
            'form': form,
            'seo_form': seo_form,
            'gallery': gallery
        })


@staff_member_required(login_url=reverse_lazy('admin:login'))
def mobile_app_page(request):
    form, gallery, seo_form, redirect_available = get_forms_in_mobile_app_page(request.POST, request.FILES, request.method)
    if redirect_available:
        return redirect(reverse_lazy('admin:mobile_app_page'))
    else:
        return render(request, 'admin/mobile-app-page.html', {
            'form': form,
            'seo_form': seo_form,
            'gallery': gallery
        })


@staff_member_required(login_url=reverse_lazy('admin:login'))
def contacts_page(request):
    cinema_contacts = utils.get_cinema_contacts()
    forms = [CinemaContactsPageForm(instance=contact, prefix=contact.cinema.name) for contact in cinema_contacts]
    if request.method == 'POST':
        forms = [CinemaContactsPageForm(request.POST, request.FILES, instance=contact, prefix=contact.cinema.name) for contact in cinema_contacts]
        for form in forms:
            if form.is_valid():
                form.save()
        return redirect(reverse_lazy('admin:cinema_contacts'))
    return render(request, 'admin/contacts_page.html', {
        'forms': forms
    })


@staff_member_required(login_url=reverse_lazy('admin:login'))
def main_page_banners(request):
    main_form, main_gallery, redirect_available = get_forms_in_banner_page(request.POST, request.FILES, request.method)

    if redirect_available:
        return redirect(reverse_lazy('admin:main_page_banners'))
    else:
        return render(request, 'admin/main_page_banners.html', {
            'main_form': main_form, 
            'main_gallery': main_gallery
        })


@staff_member_required(login_url=reverse_lazy('admin:login'))
def news_and_stocks_banners(request):
    form, gallery, redirect_available = get_forms_in_news_and_stocks_banner_page(request.POST, request.FILES, request.method)

    if redirect_available:
        return redirect(reverse_lazy('admin:news_and_stocks_page_banners'))
    else:
        return render(request, 'admin/news_and_stocks_banners.html', {
            'form': form, 
            'gallery': gallery
        })


@staff_member_required(login_url=reverse_lazy('admin:login'))
def movie_create(request):
    form = AdminMovieForm()
    seo_form = SeoParametersForm()
    gallery = Gallery(queryset=Image.objects.none(), prefix="movies_gallery")

    if request.method == 'POST':
        form = AdminMovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            seo_form = SeoParametersForm(request.POST)
            gallery = Gallery(request.POST, request.FILES, instance=movie, prefix="movies_gallery")

            if seo_form.is_valid() and gallery.is_valid():
                seo_obj = seo_form.save()
                movie.seo = seo_obj
                movie.save()
                gallery.save()

                return redirect(reverse_lazy('admin:movies'))
    return render(request, 'admin/movie_add.html', context={
        'form': form, 
        'seo_form': seo_form, 
        'gallery': gallery
    })


@staff_member_required(login_url=reverse_lazy('admin:login'))
def cinema_create(request):
    form = AdminCinemaForm()
    seo_form = SeoParametersForm()
    gallery = Gallery(queryset=Image.objects.none(), prefix="cinema_gallery")

    if request.method == 'POST':
        form = AdminCinemaForm(request.POST, request.FILES)
        if form.is_valid():
            cinema = form.save(commit=False)
            seo_form = SeoParametersForm(request.POST)
            gallery = Gallery(request.POST, request.FILES, instance=cinema, prefix="cinema_gallery")

            if seo_form.is_valid() and gallery.is_valid():
                seo_obj = seo_form.save()
                cinema.seo = seo_obj
                cinema.save()
                gallery.save()
                CinemaContactsPage.objects.create(cinema=cinema)

                return redirect(reverse_lazy('admin:cinemas'))
    return render(request, 'admin/cinema_add.html', context={
        'form': form, 
        'seo_form': seo_form, 
        'gallery': gallery
    })


@staff_member_required(login_url=reverse_lazy('admin:login'))
def hall_create(request, cinema_pk):
    cinema = utils.get_cinema_by_params(pk=cinema_pk)
    form = AdminHallForm()
    seo_form = SeoParametersForm()
    gallery = Gallery(queryset=Image.objects.none(), prefix="hall_gallery")
    if request.method == 'POST':
            form = AdminHallForm(request.POST, request.FILES)
            logger.error(form.is_valid())
            if form.is_valid():
                hall = form.save(commit=False)
                seo_form = SeoParametersForm(request.POST)
                gallery = Gallery(request.POST, request.FILES, instance=hall, prefix="hall_gallery")
                if (seo_form.is_valid() and gallery.is_valid() and
                    request.POST.get('json_scheme') is not None and request.POST.get('json_scheme')):
                    seo_obj = seo_form.save()
                    hall.seo = seo_obj
                    hall.cinema = cinema
                    hall.save()
                    gallery.save()
                    json_scheme = request.POST.get('json_scheme')
                    save_hall_places(json_scheme, hall)
                    return redirect(reverse_lazy('admin:cinema_update', kwargs={'pk': cinema_pk}))
    return render(request, 'admin/hall_add.html', {
        'form': form,
        'seo_form': seo_form, 
        'gallery': gallery,
        'cinema': cinema
    })


@staff_member_required(login_url=reverse_lazy('admin:login'))
def session_create(request):
    form = AdminSessionForm()
    form.fields['movie'].queryset = utils.get_active_movies()
    if request.method == 'POST':
        form = AdminSessionForm(request.POST)
        if form.is_valid():
            create_session(request.POST)
            return redirect(reverse_lazy('admin:sessions'))
        else:
            for k, v in form.errors.items():
                for error_message in v:
                    messages.error(request, error_message)
    return render(request, 'admin/session_create.html', {
        'form': form
    })


@staff_member_required(login_url=reverse_lazy('admin:login'))
def update_session_info(request, pk):
    session = utils.get_session_by_params(pk=pk)
    form = AdminSessionForm(instance=session)
    form.fields['movie'].queryset = utils.get_active_movies()
    rows = max(place.real_row for place in session.hall.ordered_places)
    cols = max(place.real_position for place in session.hall.ordered_places)
    px = 50
    if cols > 17 and cols < 20:
        px = 45
    elif cols > 19 and cols < 22:
        px = 40
    elif cols >= 22 and cols < 24:
        px = 35
    elif cols >= 24 and cols < 27:
        px = 30
    elif cols >= 27:
        px = 27
    users = User.objects.all()
    if request.method == 'POST':
        form = AdminSessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('admin:session_update', kwargs={'pk': session.pk}))
        else:
            logger.error(form.errors.items())
    return render(request, 'admin/session_update.html', {
        'form': form,
        'rows': range(1, rows + 1),
        'cols': range(1, cols + 1),
        'px': px,
        'users': users,
    })


@staff_member_required(login_url=reverse_lazy('admin:login'))
def news_create(request):
    form = AdminNewsForm()
    seo_form = SeoParametersForm()
    gallery = Gallery(queryset=Image.objects.none(), prefix="news_gallery")

    if request.method == 'POST':
        form = AdminNewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            seo_form = SeoParametersForm(request.POST)
            gallery = Gallery(request.POST, request.FILES, instance=news, prefix="news_gallery")

            if seo_form.is_valid() and gallery.is_valid():
                seo_obj = seo_form.save()
                news.seo = seo_obj
                news.save()
                gallery.save()

                return redirect(reverse_lazy('admin:news'))
    return render(request, 'admin/news_add.html', context={
        'form': form, 
        'seo_form': seo_form, 
        'gallery': gallery
    })


@staff_member_required(login_url=reverse_lazy('admin:login'))
def stock_create(request):
    form = AdminStockForm()
    seo_form = SeoParametersForm()
    gallery = Gallery(queryset=Image.objects.none(), prefix="stock_gallery")

    if request.method == 'POST':
        form = AdminStockForm(request.POST, request.FILES)
        if form.is_valid():
            stock = form.save(commit=False)
            seo_form = SeoParametersForm(request.POST)
            gallery = Gallery(request.POST, request.FILES, instance=stock, prefix="stock_gallery")

            if seo_form.is_valid() and gallery.is_valid():
                seo_obj = seo_form.save()
                stock.seo = seo_obj
                stock.save()
                gallery.save()

                return redirect(reverse_lazy('admin:stocks'))
    return render(request, 'admin/stock_add.html', context={
        'form': form, 
        'seo_form': seo_form, 
        'gallery': gallery
    })


@staff_member_required(login_url=reverse_lazy('admin:login'))
def update_movie_info(request, pk):
    movie = utils.get_movie_by_params(pk=pk)
    form = AdminMovieForm(instance=movie)
    seo_form = SeoParametersForm(instance=movie.seo)
    extra_count = 4 - movie.gallery.all().count() % 4
    extra_count = 0 if extra_count == 4 and movie.gallery.all().count() > 0 else extra_count
    UpdateGallery = generic_inlineformset_factory(Image, can_delete=True,
        extra=extra_count)
    gallery = UpdateGallery(request.POST or None, request.FILES or None, queryset=movie.gallery.all(), instance=movie, prefix="movies_gallery")
    if request.method == 'POST':
        form = AdminMovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            movie = form.save(commit=False)
            seo_form = SeoParametersForm(request.POST)

            if seo_form.is_valid() and gallery.is_valid():
                seo_obj = seo_form.save()
                movie.seo = seo_obj
                movie.save()
                gallery.save()
                return redirect(reverse_lazy('admin:movies'))
    return render(request, 'admin/movie_update.html', context={
        'form': form, 
        'seo_form': seo_form, 
        'gallery': gallery
    })


@staff_member_required(login_url=reverse_lazy('admin:login'))
def update_cinema_info(request, pk):
    cinema = utils.get_cinema_by_params(pk=pk)
    form = AdminCinemaForm(instance=cinema)
    seo_form = SeoParametersForm(instance=cinema.seo)
    extra_count = 4 - cinema.gallery.all().count() % 4
    extra_count = 0 if extra_count == 4 and cinema.gallery.all().count() > 0 else extra_count
    UpdateGallery = generic_inlineformset_factory(Image, can_delete=True,
        extra=extra_count)
    gallery = UpdateGallery(request.POST or None, request.FILES or None, queryset=cinema.gallery.all(), instance=cinema, prefix="cinema_gallery")
    halls = utils.get_cinema_halls(cinema.pk)
    if request.method == 'POST':
        form = AdminCinemaForm(request.POST, request.FILES, instance=cinema)
        if form.is_valid():
            cinema = form.save(commit=False)
            seo_form = SeoParametersForm(request.POST)

            if seo_form.is_valid() and gallery.is_valid():
                seo_obj = seo_form.save()
                cinema.seo = seo_obj
                cinema.save()
                gallery.save()
                return redirect(reverse_lazy('admin:cinemas'))
    return render(request, 'admin/cinema_update.html', context={
        'form': form, 
        'seo_form': seo_form, 
        'gallery': gallery,
        'halls': halls
    })


@staff_member_required(login_url=reverse_lazy('admin:login'))
def update_hall_info(request, cinema_pk, pk):
    cinema = utils.get_cinema_by_params(pk=cinema_pk)
    hall = utils.get_hall_by_params(pk=pk)
    rows = max(place.real_row for place in hall.ordered_places)
    cols = max(place.real_position for place in hall.ordered_places)
    px = 50
    if cols > 17 and cols < 20:
        px = 45
    elif cols > 19 and cols < 22:
        px = 40
    elif cols >= 22 and cols < 24:
        px = 35
    elif cols >= 24 and cols < 27:
        px = 30
    elif cols >= 27:
        px = 27
    form = AdminHallForm(instance=hall)
    seo_form = SeoParametersForm(instance=hall.seo)
    extra_count = 4 - hall.gallery.all().count() % 4
    extra_count = 0 if extra_count == 4 and hall.gallery.all().count() > 0 else extra_count
    UpdateGallery = generic_inlineformset_factory(Image, can_delete=True,
        extra=extra_count)
    gallery = UpdateGallery(request.POST or None, request.FILES or None, queryset=hall.gallery.all(), instance=hall, prefix="hall_gallery")
    if request.method == 'POST':
        form = AdminHallForm(request.POST, request.FILES, instance=hall)
        if form.is_valid():
            hall = form.save(commit=False)
            seo_form = SeoParametersForm(request.POST)
            if seo_form.is_valid() and gallery.is_valid():
                seo_obj = seo_form.save()
                hall.seo = seo_obj
                hall.save()
                gallery.save()
                if request.POST.get('json_scheme') is not None and request.POST.get('json_scheme'):
                    json_scheme = request.POST.get('json_scheme')
                    update_hall_places(json_scheme, hall)
                return redirect(reverse_lazy('admin:cinema_update', kwargs={'pk': cinema_pk}))
    return render(request, 'admin/hall_update.html', context={
        'form': form, 
        'seo_form': seo_form, 
        'gallery': gallery,
        'cinema': cinema,
        'rows': range(1, rows + 1),
        'cols': range(1, cols + 1),
        'px': px,
    })


@staff_member_required(login_url=reverse_lazy('admin:login'))
def update_news_info(request, pk):
    news = utils.get_news_object_by_params(pk=pk)
    form = AdminNewsForm(instance=news)
    seo_form = SeoParametersForm(instance=news.seo)
    extra_count = 4 - news.gallery.all().count() % 4
    extra_count = 0 if extra_count == 4 and news.gallery.all().count() > 0 else extra_count
    UpdateGallery = generic_inlineformset_factory(Image, can_delete=True,
        extra=extra_count)
    gallery = UpdateGallery(request.POST or None, request.FILES or None, 
        queryset=news.gallery.all(), instance=news, prefix="news_gallery")
    if request.method == 'POST':
        form = AdminNewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            news = form.save(commit=False)
            seo_form = SeoParametersForm(request.POST)

            if seo_form.is_valid() and gallery.is_valid():
                seo_obj = seo_form.save()
                news.seo = seo_obj
                logger.info(news.main_image)
                news.save()
                gallery.save()
                return redirect(reverse_lazy('admin:news'))
    return render(request, 'admin/news_update.html', context={
        'form': form, 
        'seo_form': seo_form, 
        'gallery': gallery
    })


@staff_member_required(login_url=reverse_lazy('admin:login'))
def update_stock_info(request, pk):
    stock = utils.get_stock_by_params(pk=pk)
    form = AdminStockForm(instance=stock)
    seo_form = SeoParametersForm(instance=stock.seo)
    extra_count = 4 - stock.gallery.all().count() % 4
    extra_count = 0 if extra_count == 4 and stock.gallery.all().count() > 0 else extra_count
    UpdateGallery = generic_inlineformset_factory(Image, can_delete=True,
        extra=extra_count)
    gallery = UpdateGallery(request.POST or None, request.FILES or None, 
        queryset=stock.gallery.all(), instance=stock, prefix="stock_gallery")
    if request.method == 'POST':
        form = AdminStockForm(request.POST, request.FILES, instance=stock)
        if form.is_valid():
            stock = form.save(commit=False)
            seo_form = SeoParametersForm(request.POST)

            if seo_form.is_valid() and gallery.is_valid():
                seo_obj = seo_form.save()
                stock.seo = seo_obj
                stock.save()
                gallery.save()
                return redirect(reverse_lazy('admin:stocks'))
    return render(request, 'admin/stock_update.html', context={
        'form': form, 
        'seo_form': seo_form, 
        'gallery': gallery
    })


@staff_member_required(login_url=reverse_lazy('admin:login'))
@require_http_methods(['DELETE'])
def api_delete_image(request, pk):
    image = utils.get_image_by_id(pk)
    image.delete()
    return JsonResponse({})


@staff_member_required(login_url=reverse_lazy('admin:login'))
@require_http_methods(['DELETE'])
def api_delete_movie(request, pk):
    movie = utils.get_movie_by_params(pk=pk)
    movie.delete()
    return JsonResponse({})


@staff_member_required(login_url=reverse_lazy('admin:login'))
@require_http_methods(['DELETE'])
def api_delete_cinema(request, pk):
    cinema = utils.get_cinema_by_params(pk=pk)
    cinema.delete()
    return JsonResponse({})


@staff_member_required(login_url=reverse_lazy('admin:login'))
@require_http_methods(['DELETE'])
def api_delete_hall(request, pk):
    hall = utils.get_hall_by_params(pk=pk)
    hall.delete()
    return JsonResponse({})


@staff_member_required(login_url=reverse_lazy('admin:login'))
@require_http_methods(['DELETE'])
def api_delete_news_object(request, pk):
    news_object = utils.get_news_object_by_params(pk=pk)
    news_object.delete()
    return JsonResponse({})


@staff_member_required(login_url=reverse_lazy('admin:login'))
@require_http_methods(['DELETE'])
def api_delete_stock(request, pk):
    stock = utils.get_stock_by_params(pk=pk)
    stock.delete()
    return JsonResponse({})


@staff_member_required(login_url=reverse_lazy('admin:login'))
@require_http_methods(['DELETE'])
def api_delete_user(request, email):
    user = get_user_by_email(email)
    user.delete()
    return JsonResponse({})


@staff_member_required(login_url=reverse_lazy('admin:login'))
@require_http_methods(['DELETE'])
def api_delete_html_email(request, pk):
    html_email = get_object_or_404(Mail, pk=pk)
    html_email.delete()
    return JsonResponse({})

class MovieListView(ListView):
    model = Movie
    queryset = utils.get_active_movies()
    context_object_name = 'active_movies'
    template_name = 'admin/movies_list.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['soon_movies'] = utils.get_soon_movies()
        context['retired_movies'] = utils.get_retired_movies()
        return context


class CinemaListView(ListView):
    model = Cinema
    queryset = utils.get_cinemas()
    context_object_name = 'cinemas'
    template_name = 'admin/cinemas_list.html'


class SessionListView(ListView):
    model = Session
    queryset = utils.get_future_sessions().order_by('time')
    context_object_name = 'sessions'
    template_name = 'admin/session_list.html'


class NewsListView(ListView):
    model = News
    queryset = utils.get_news()
    context_object_name = 'news'
    template_name = 'admin/news_list.html'


class StockListView(ListView):
    model = Stock
    queryset = utils.get_stocks()
    context_object_name = 'stocks'
    template_name = 'admin/stock_list.html'


class UserListView(ListView):
    model = User
    queryset = User.objects.all()
    context_object_name = 'users'
    template_name = 'admin/users_list.html'


def login(request):
    form = LoginForm()

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            if user.is_staff:
                redirect_to = request.POST.get('next')
                if redirect_to:
                    return redirect(redirect_to)
                return redirect(reverse_lazy('admin:index'))
            else:
                messages.error(request, 'Вход разрешён только сотрудникам')
        else:
            user = get_user_by_email(email)
            if user is None:
                messages.error(request, 'Пользователя с такими данными не найдено')
            elif user is not None and user.is_active == False:
                messages.error(request, 'Пользователь заблокирован')
            elif not user.is_staff:
                messages.error(request, 'Вход разрешён только сотрудникам')
            form = LoginForm(request.POST)
            # return render(request, 'users/log.html', context={'signup_form': signup_form, 'login_form': login_form, 'signup':False})
    return render(request, 'admin/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect(reverse_lazy('admin:login'))


@staff_member_required(login_url=reverse_lazy('admin:login'))
def change_user_info(request, email):
    user = get_user_by_email(email)
    form = UserUpdateForm(request.POST or None, instance=user)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('admin:users'))
    return render(request, 'admin/user_update.html', {'form':form})


@staff_member_required(login_url=reverse_lazy('admin:login'))
def create_user(request):
    form = UserCreateForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('admin:users'))
    return render(request, 'admin/user_create.html', {'form':form})


@staff_member_required(login_url=reverse_lazy('admin:login'))
def mailing(request):
    mails = Mail.objects.order_by('-uploaded')[:5]
    form = MailingForm(initial={'recipients': '0'})
    if request.method == 'POST':
        make_mailing(request)
    return render(request, 'admin/mailing.html', {
        'form': form, 
        'mails':mails,
        'users': User.objects.all()
    })


@staff_member_required(login_url=reverse_lazy('admin:login'))
@require_http_methods(['POST'])
def api_update_session_ticket(request, pk):
    ticket = utils.get_ticket_by_params(pk=pk)
    session = ticket.session
    ticket.status = request.POST.get('status')
    if ticket.status != '0':
        ticket.user = get_user_by_email(request.POST.get('user_email'))
    else:
        ticket.user = None
    ticket.save()
    return JsonResponse({
        'total_places': session.total_places,
        'total_free_places': session.total_free_places,
        'total_booked_places': session.total_booked_places,
        'booked_money': session.booked_money,
        'total_sold_places': session.total_sold_places,
        'sold_money': session.sold_money
    })


@staff_member_required(login_url=reverse_lazy('admin:login'))
@require_http_methods(['GET'])
def api_is_any_planned_sessions_in_hall(request, hall_pk):
    sessions = utils.get_future_sessions().filter(hall=utils.get_hall_by_params(pk=hall_pk))
    responce = {}
    if sessions.count() > 0:
        responce['any'] = True
    else:
        responce['any'] = False
    return JsonResponse(responce)