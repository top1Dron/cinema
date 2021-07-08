from datetime import date, timedelta, datetime as dt
import logging
import textwrap

from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView, ListView

from app.forms import UserCreateForm, UserUpdateForm, SessionFilterForm
from app.models import NewsAndStockBanner, News, Session, Stock
from app import utils
from users.forms import LoginForm
from users.utils import get_user_by_email


logger = logging.getLogger(__name__)


def index(request):
    news_and_stocks_range = range(NewsAndStockBanner.load().gallery.count())
    today_movies = utils.get_today_movies()
    soon_movies = utils.get_soon_movies()
    for m in today_movies:
        m.name = textwrap.shorten(m.name, 20, placeholder='...')
        m.name_uk = textwrap.shorten(m.name_uk, 20, placeholder='...')
    for m in soon_movies:
        m.name = textwrap.shorten(m.name, 20, placeholder='...')
        m.name_uk = textwrap.shorten(m.name_uk, 20, placeholder='...')
    return render(request, 'main.html', {
        'news_and_stocks_range': news_and_stocks_range,
        'today_movies': today_movies,
        'today': date.today(),
        'soon_movies': soon_movies,
    })


def cafe_bar_page(request):
    return render(request, 'cafe-bar-page.html')


def advertise_page(request):
    return render(request, 'advertise-page.html')


def about_cinema(request):
    return render(request, 'about-cinema.html')


def mobile_app_page(request):
    return render(request, 'mobile-app.html')


def children_room_page(request):
    return render(request, 'children-room.html')


def contacts_page(request):
    contacts = utils.get_cinema_contacts()
    return render(request, 'contacts-page.html', {
        'contacts': contacts
    })


def news_list(request):
    news = utils.get_active_news()
    return render(request, 'news-list.html', {'news': news})


class NewsDetailView(DetailView):
    model = News
    context_object_name = 'article'
    template_name = 'news_detail.html'


def stocks_list(request):
    stocks = utils.get_active_stocks()
    return render(request, 'stocks-list.html', {'stocks': stocks})


class StockDetailView(DetailView):
    model = Stock
    context_object_name = 'article'
    template_name = 'stock_detail.html'


def signup(request):
    form = UserCreateForm()
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(
                request, 
                email=user.email,
                password=request.POST.get('password1'))
            auth_login(request, user)
            return redirect(reverse_lazy('app:index'))
    return render(request, 'registration.html',{'form': form})


@login_required
def profile(request):
    user = request.user
    form = UserUpdateForm(request.POST or None, instance=user)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            user.set_password(form.cleaned_data['password1'])
            user.save()
            user = authenticate(
                request, 
                email=user.email,
                password=request.POST.get('password1'))
            auth_login(request, user)
            return redirect(reverse_lazy('app:index'))
    return render(request, 'profile.html', {'form':form})


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
            return redirect(reverse_lazy('app:index'))
        else:
            user = get_user_by_email(email)
            if user is None:
                messages.error(request, 'Пользователя с такими данными не найдено')
            elif user is not None and user.is_active == False:
                messages.error(request, 'Пользователь заблокирован')
            else:
                messages.error(request, 'Пароль неверный')
            form = LoginForm(request.POST)
    return render(request, 'login.html', {'form': form})


@login_required
def logout_user(request):
    logout(request)
    return redirect(reverse_lazy('app:index'))


def cinemas_list(request):
    cinema_list = utils.get_cinemas()
    for c in cinema_list:
        c.name = textwrap.shorten(c.name, 20, placeholder='...')
        c.name_uk = textwrap.shorten(c.name_uk, 20, placeholder='...')
    return render(request, 'cinemas.html', {
        'cinemas': cinema_list
    })


def cinema_detail(request, pk):
    cinema = utils.get_cinema_by_params(pk=pk)
    today_sessions = utils.get_today_sessions_in_cinema(cinema)
    return render(request, 'cinema_detail.html', {
        'cinema': cinema,
        'today_sessions': today_sessions,
    })


def hall_detail(request, pk):
    hall = utils.get_hall_by_params(pk=pk)
    today_sessions = utils.get_today_sessions_in_hall(hall)
    rows = max(place.real_row for place in hall.ordered_places)
    cols = max(place.real_position for place in hall.ordered_places)
    return render(request, 'hall_detail.html', {
        'hall': hall,
        'today_sessions': today_sessions,
        'rows': range(1, rows + 1),
        'cols': range(1, cols + 1),
    })


def afiche(request):
    active_movies = utils.get_active_movies()
    soon_movies = utils.get_soon_movies()
    for m in active_movies:
        m.name = textwrap.shorten(m.name, 20, placeholder='...')
        m.name_uk = textwrap.shorten(m.name_uk, 20, placeholder='...')
    for m in soon_movies:
        m.name = textwrap.shorten(m.name, 20, placeholder='...')
        m.name_uk = textwrap.shorten(m.name_uk, 20, placeholder='...')
    return render(request, 'afiche.html', {
        'active_movies': active_movies,
        'soon_movies': soon_movies
    })


def soon(request):
    active_movies = utils.get_active_movies()
    soon_movies = utils.get_soon_movies()
    for m in active_movies:
        m.name = textwrap.shorten(m.name, 20, placeholder='...')
        m.name_uk = textwrap.shorten(m.name_uk, 20, placeholder='...')
    for m in soon_movies:
        m.name = textwrap.shorten(m.name, 20, placeholder='...')
        m.name_uk = textwrap.shorten(m.name_uk, 20, placeholder='...')
    return render(request, 'soon.html', {
        'active_movies': active_movies,
        'soon_movies': soon_movies
    })


class SheduleListView(ListView):
    model = Session
    context_object_name = 'sessions'
    template_name = 'shedule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = SessionFilterForm()
        if 'movie' in self.request.GET:
            context['filter_form'].fields['movie'].initial = self.request.GET.get('movie')
        if 'cinema' in self.request.GET:
            context['filter_form'].fields['cinema'].initial = self.request.GET.get('cinema')
        if 'format' in self.request.GET:
            context['filter_form'].fields['format'].initial = self.request.GET.get('format')
        today_sessions = self.get_queryset().filter(time__day=timezone.now().today().day, time__month=timezone.now().today().month, time__year=timezone.now().today().year)
        for s in today_sessions:
            s.movie.name = textwrap.shorten(s.movie.name, 20, placeholder='...')
            s.movie.name_uk = textwrap.shorten(s.movie.name_uk, 20, placeholder='...')
            s.hall.cinema.name = textwrap.shorten(s.hall.cinema.name, 20, placeholder='...')
            s.hall.cinema.name_uk = textwrap.shorten(s.hall.cinema.name_uk, 20, placeholder='...')
        context['today_sessions'] = today_sessions
        tomorrow = timezone.now().today() + timedelta(days=1)
        tomorrow_sessions = self.get_queryset().filter(time__day=tomorrow.day, time__month=tomorrow.month, time__year=tomorrow.year)
        for s in tomorrow_sessions:
            s.movie.name = textwrap.shorten(s.movie.name, 20, placeholder='...')
            s.movie.name_uk = textwrap.shorten(s.movie.name_uk, 20, placeholder='...')
            s.hall.cinema.name = textwrap.shorten(s.hall.cinema.name, 20, placeholder='...')
            s.hall.cinema.name_uk = textwrap.shorten(s.hall.cinema.name_uk, 20, placeholder='...')
        context['tomorrow_sessions'] = tomorrow_sessions
        next_week_sessions = self.get_queryset().filter(time__gte=timezone.now(), time__lte=timezone.now() + timedelta(days=7))
        for s in next_week_sessions:
            s.movie.name = textwrap.shorten(s.movie.name, 20, placeholder='...')
            s.movie.name_uk = textwrap.shorten(s.movie.name_uk, 20, placeholder='...')
            s.hall.cinema.name = textwrap.shorten(s.hall.cinema.name, 20, placeholder='...')
            s.hall.cinema.name_uk = textwrap.shorten(s.hall.cinema.name_uk, 20, placeholder='...')
        context['next_week_sessions'] = next_week_sessions
        return context

    def get_queryset(self):
        queryset = utils.get_future_sessions()
        if 'movie' in self.request.GET:
            queryset = utils.get_sessions_by_movie(
                sessions=queryset, 
                movie_pk=self.request.GET.get('movie'))
        if 'cinema' in self.request.GET:
            queryset = utils.get_sessions_by_cinema(
                sessions=queryset, 
                cinema_pk=self.request.GET.get('cinema'))
        if 'format' in self.request.GET:
            queryset = utils.get_sessions_by_format(
                sessions=queryset, 
                format=self.request.GET.get('format'))
        if 'hall' in self.request.GET:
            queryset = utils.get_sessions_by_hall(
                sessions=queryset, 
                hall_pk=self.request.GET.get('hall'))
        for s in queryset:
            s.movie.name = textwrap.shorten(s.movie.name, 20, placeholder='...')
            s.movie.name_uk = textwrap.shorten(s.movie.name_uk, 20, placeholder='...')
            s.hall.cinema.name = textwrap.shorten(s.hall.cinema.name, 20, placeholder='...')
            s.hall.cinema.name_uk = textwrap.shorten(s.hall.cinema.name_uk, 20, placeholder='...')
        return queryset


def movie_detail(request, pk):
    movie = utils.get_movie_by_params(pk=pk)
    sessions = utils.get_sessions_by_movie(
        sessions=utils.get_future_sessions(),
        movie_pk=movie.pk
    )
    return render(request, 'movie_detail.html', {'movie': movie, 'sessions': sessions})


@login_required
def book_tickets_for_session(request, pk):
    if request.method == 'POST':
        tickets = request.POST.get('selected_tickets_book')
        for ticket_id in tickets.split(' '):
            ticket = utils.get_ticket_by_params(pk=int(ticket_id))
            ticket.user = request.user
            ticket.status = '1'
            ticket.save()
        return redirect(reverse_lazy('app:book_tickets_for_session', kwargs={'pk': pk}))
    session = utils.get_session_by_params(pk=pk)
    rows = max(place.real_row for place in session.hall.ordered_places)
    cols = max(place.real_position for place in session.hall.ordered_places)
    return render(request, 'book-ticket-for-session.html', {
        'session': session,
        'rows': range(1, rows + 1),
        'cols': range(1, cols + 1),
    })


@login_required
@require_http_methods(['POST'])
def buy_tickets_for_session(request, pk):
    tickets = request.POST.get('selected_tickets_buy')
    for ticket_id in tickets.split(' '):
        ticket = utils.get_ticket_by_params(pk=int(ticket_id))
        ticket.user = request.user
        ticket.status = '2'
        ticket.save()
    return redirect(reverse_lazy('app:book_tickets_for_session', kwargs={'pk': pk}))


@login_required
def view_user_tickets(request):
    active_tickets = utils.get_active_user_tickets(request.user)
    expired_tickets = utils.get_expired_user_tickets(request.user)
    return render(request, 'user_tickets.html', {
        'active_tickets': active_tickets,
        'expired_tickets': expired_tickets,
    })


@login_required
def return_a_ticket(request, pk):
    ticket = utils.get_ticket_by_params(pk=pk)
    ticket.status = '0'
    ticket.user = get_user_by_email('admin1@gmail.com')
    ticket.save()
    return redirect(reverse_lazy('app:view_user_tickets'))


@login_required
def buy_the_ticket(request, pk):
    ticket = utils.get_ticket_by_params(pk=pk)
    ticket.status = '2'
    ticket.save()
    return redirect(reverse_lazy('app:view_user_tickets'))


def find_movie(request):
    url_param = request.GET.get('nameContains')
    logger.info(url_param)
    data = utils.find_movies_by_param(url_param)
    logger.info(data)
    return JsonResponse(data, safe=False)
