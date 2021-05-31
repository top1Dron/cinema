import logging
from PIL import Image

from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.forms import utils
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView

from app.models import Movie, Image
from app.forms import MovieForm, SeoParametersForm, Gallery, ImageForm
from app.utils import get_movie_by_params, get_image_by_id


logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'admin/statistics.html')


# class MovieCreateView(CreateView):
#     model = Movie
#     form_class = MovieForm
#     template_name = 'admin/movie_add.html'

#     def get_context_data(self, **kwargs) -> dict:
#         context = super().get_context_data(**kwargs)
#         context['image_forms'] = Gallery
#         context['seo_form'] = SeoParametersForm()
#         return context

#     def form_valid(self, form):
#         logger.info(form.instance)
#         logger.info(self.request.POST)

#     def post(self, request, *args, **kwargs):
#         logger.info(request.POST)
#         logger.info(request.FILES)
#         form = MovieForm(request.POST, request.FILES)
#         movie = form.save(commit=False)
        
#         gallery = Gallery(request.POST, request.FILES, instance=movie)
#         logger.info(gallery.is_valid())
#         for img_form in gallery:
#             logger.info(img_form.errors)
#             logger.info(img_form.cleaned_data)
#         logger.info(f'{img.width} x {img.height}')


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

def update_movie_info(request, pk):
    movie = get_movie_by_params(pk=pk)
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

@require_http_methods(['DELETE'])
def api_delete_image(request, pk):
    image = get_image_by_id(pk)
    image.delete()
    return JsonResponse({})
