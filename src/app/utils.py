from datetime import date as dt, datetime
import logging

from django.shortcuts import get_object_or_404

from app.models import Cinema, Movie, Image, News, Stock, Hall, Session, Ticket


logger = logging.getLogger(__name__)


def get_movie_by_params(**kwargs):
    return get_object_or_404(Movie, **kwargs)


def get_cinema_by_params(**kwargs):
    return get_object_or_404(Cinema, **kwargs)


def get_hall_by_params(**kwargs):
    return get_object_or_404(Hall, **kwargs)


def get_session_by_params(**kwargs):
    return get_object_or_404(Session, **kwargs)

def get_ticket_by_params(**kwargs):
    return get_object_or_404(Ticket, **kwargs)

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


def get_cinemas():
    return Cinema.objects.all().select_related('seo')


def get_cinema_halls(cinema_id):
    return Hall.objects.filter(cinema=get_cinema_by_params(pk=cinema_id))


def get_news_object_by_params(**kwargs):
    return get_object_or_404(News, **kwargs)


def get_news():
    return News.objects.all().select_related('seo')


def get_stock_by_params(**kwargs):
    return get_object_or_404(Stock, **kwargs)


def get_stocks():
    return Stock.objects.all().select_related('seo')


def get_future_sessions():
    return Session.objects.filter(time__gte=datetime.now())
