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

from users.forms import LoginForm
from users.utils import get_user_by_email
from app.models import Image, Movie
from app.forms import MovieForm, SeoParametersForm, Gallery
from app import utils


logger = logging.getLogger(__name__)

@staff_member_required(login_url=reverse_lazy('admin:login'))
def index(request):
    return render(request, 'admin/statistics.html')


@staff_member_required(login_url=reverse_lazy('admin:login'))
def movie_create(request):
    form = MovieForm()
    seo_form = SeoParametersForm()
    gallery = Gallery(queryset=Image.objects.none())

    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            seo_form = SeoParametersForm(request.POST)
            gallery = Gallery(request.POST, request.FILES, instance=movie)

            if seo_form.is_valid():
                seo_obj = seo_form.save()
                movie.seo = seo_obj
                movie.save()
                if gallery.is_valid():
                    gallery.save()

                return redirect(reverse_lazy('admin:movie_update', kwargs={'pk': movie.pk}))
    return render(request, 'admin/movie_add.html', context={
        'form': form, 
        'seo_form': seo_form, 
        'gallery': gallery
    })


@staff_member_required(login_url=reverse_lazy('admin:login'))
def update_movie_info(request, pk):
    movie = utils.get_movie_by_params(pk=pk)
    form = MovieForm(instance=movie)
    seo_form = SeoParametersForm(instance=movie.seo)
    extra_count = 4 - movie.gallery.all().count() % 4
    extra_count = 0 if extra_count == 4 else extra_count
    UpdateGallery = generic_inlineformset_factory(Image, can_delete=True,
        extra=extra_count)
    gallery = UpdateGallery(request.POST or None, request.FILES or None, queryset=movie.gallery.all(), instance=movie)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            movie = form.save(commit=False)
            seo_form = SeoParametersForm(request.POST)

            if seo_form.is_valid():
                seo_obj = seo_form.save()
                movie.seo = seo_obj
                movie.save()
            if gallery.is_valid():
                gallery.save()
            if form.is_valid() and seo_form.is_valid():
                return redirect(reverse_lazy('admin:movie_update', kwargs={'pk': movie.pk}))
    return render(request, 'admin/movie_update.html', context={
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


def login(request):
    form = LoginForm()

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            redirect_to = request.POST.get('next')
            if redirect_to:
                return redirect(redirect_to)
            return redirect(reverse_lazy('admin:index'))
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