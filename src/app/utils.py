from calendar import monthrange
from datetime import date as dt, datetime, timedelta
import logging
import textwrap

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls.base import reverse_lazy
from django.utils import timezone

from app.models import Cinema, Movie, Image, News, Stock, Hall, Session, Ticket, CinemaContactsPage


logger = logging.getLogger(__name__)


def find_movies_by_param(param):
    movies = Movie.objects.filter(
        Q(name_ru__icontains=param) | 
        Q(name_uk__icontains=param)
    )
    return [{'detail_link': reverse_lazy('app:movie_detail', kwargs={'pk': movie.pk}), 'name_ru': movie.name_ru} for movie in movies]


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
    return get_not_active_movies().filter(release_date__gt=dt.today())


def get_retired_movies():
    return get_not_active_movies().filter(release_date__lte=dt.today())


def get_today_movies():
    today_sessions = Session.objects.filter(time__year=dt.today().year, time__month=dt.today().month, time__day=dt.today().day)
    return set(s.movie for s in today_sessions)


def get_cinemas():
    return Cinema.objects.all().select_related('seo')


def get_cinema_halls(cinema_id):
    return Hall.objects.filter(cinema=get_cinema_by_params(pk=cinema_id)).order_by('number')


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


def get_active_user_tickets(user):
    return Ticket.objects.filter(user=user, session__time__gte=timezone.now())


def get_expired_user_tickets(user):
    return Ticket.objects.filter(user=user, session__time__lt=timezone.now())


def get_month_sessions():
    month_sessions = {}
    start_date = dt(dt.today().year, dt.today().month, 1)
    end_date = dt(dt.today().year, dt.today().month, monthrange(dt.today().year, dt.today().month)[1])
    delta = end_date - start_date
    for i in range(delta.days + 1):
        sessions_date = start_date + timedelta(days=i)
        month_sessions[f'{sessions_date.day}.{sessions_date.month}.{sessions_date.year}'] = \
            Session.objects.filter(
                time__year=sessions_date.year, 
                time__month=sessions_date.month, 
                time__day=sessions_date.day
            ).count()
    return dt.today().month, month_sessions


def get_movies_fees():
    movies_fees = {movie.name: 0 for movie in Movie.objects.all()}
    for movie_name in movies_fees:
        movie = get_movie_by_params(name=movie_name)
        movie_sessions = Session.objects.filter(movie=movie)
        sold_tickets = Ticket.objects.filter(session__in=movie_sessions, status='2')
        fee = 0.0
        for ticket in sold_tickets:
            if ticket.place.is_vip:
                fee += ticket.session.vip_price
            else:
                fee += ticket.session.price
        movies_fees[movie.name] = int(fee)
        movies_fees = {textwrap.shorten(k, 20, placeholder='...'): v for k, v in sorted(movies_fees.items(), key=lambda x: -x[1])[:10] if v > 0}
    return movies_fees