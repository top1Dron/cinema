from datetime import date as dt, datetime
import logging

from django.shortcuts import get_object_or_404

from app.models import Cinema, Movie, Image, News, Stock, Hall, Session, Ticket, CinemaContactsPage


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


def get_today_movies():
    today_sessions = Session.objects.filter(time__year=dt.today().year, time__month=dt.today().month, time__day=dt.today().day)
    return set(s.movie for s in today_sessions)


def get_cinemas():
    return Cinema.objects.all().select_related('seo')


def get_cinema_halls(cinema_id):
    return Hall.objects.filter(cinema=get_cinema_by_params(pk=cinema_id))


def get_news_object_by_params(**kwargs):
    return get_object_or_404(News, **kwargs)


def get_news():
    return News.objects.all().select_related('seo')


def get_active_news():
    return get_news().filter(status=True)


def get_stock_by_params(**kwargs):
    return get_object_or_404(Stock, **kwargs)


def get_stocks():
    return Stock.objects.all().select_related('seo')


def get_active_stocks():
    return get_stocks().filter(status=True)


def get_future_sessions():
    return Session.objects.filter(time__gte=datetime.now())


def get_cinema_contacts():
    return CinemaContactsPage.objects.all()


def get_today_sessions_in_cinema(cinema):
    return get_today_sessions().filter(hall__cinema=cinema)


def get_today_sessions_in_hall(hall):
    return get_today_sessions().filter(hall=hall)


def get_today_sessions():
    return Session.objects.filter(
        time__day=dt.today().day, 
        time__month=dt.today().month, 
        time__year=dt.today().year)


def get_sessions_by_movie(sessions, movie_pk):
    return sessions.filter(movie=get_movie_by_params(pk=movie_pk))


def get_sessions_by_cinema(sessions, cinema_pk):
    return sessions.filter(hall__cinema=get_cinema_by_params(pk=cinema_pk))


def get_sessions_by_hall(sessions, hall_pk):
    return sessions.filter(hall=get_hall_by_params(pk=hall_pk))


def get_sessions_by_format(sessions, format):
    return sessions.filter(format=format)