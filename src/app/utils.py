from datetime import date as dt
import logging

from django.shortcuts import get_object_or_404

from app.models import Movie, Image, News, Stock


logger = logging.getLogger(__name__)


def get_movie_by_params(**kwargs):
    return get_object_or_404(Movie, **kwargs)


def get_image_by_id(id):
    return get_object_or_404(Image, id=id)


def get_active_movies():
    return Movie.objects.filter(is_active=True).select_related('seo')


def get_not_active_movies():
    return Movie.objects.filter(is_active=False).select_related('seo')


def get_soon_movies():
    return get_not_active_movies().filter(release_date__gte=dt.today())


def get_retired_movies():
    return get_not_active_movies().filter(release_date__lte=dt.today())


def get_news_object_by_params(**kwargs):
    return get_object_or_404(News, **kwargs)


def get_news():
    return News.objects.all().select_related('seo')


def get_stock_by_params(**kwargs):
    return get_object_or_404(News, **kwargs)


def get_stocks():
    return Stock.objects.all().select_related('seo')
