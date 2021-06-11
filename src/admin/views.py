import logging
from PIL import Image

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.forms import utils
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView

from app.models import Image, Movie, News, Stock, MainPage
from admin.forms import AdminMovieForm, AdminNewsForm, AdminStockForm, SeoParametersForm, Gallery
from admin.utils import get_forms_in_banner_page, get_forms_in_news_and_stocks_banner_page, get_forms_in_main_page, get_forms_in_cafe_bar_pages
from app import utils
from users.forms import LoginForm
from users.utils import get_user_by_email


logger = logging.getLogger(__name__)

@staff_member_required(login_url=reverse_lazy('admin:login'))
def index(request):
    return render(request, 'admin/statistics.html')


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
    extra_count = 0 if extra_count == 4 else extra_count
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
    extra_count = 0 if extra_count == 4 else extra_count
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