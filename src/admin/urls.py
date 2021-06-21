from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path, reverse_lazy

from admin import views


app_name = 'admin'


urlpatterns = [
    path('ajax/delete-image/<int:pk>/', views.api_delete_image, name='delete_image'),
    path('ajax/delete-movie/<int:pk>/', views.api_delete_movie, name='movie_delete'),
    path('ajax/delete-cinema/<int:pk>/', views.api_delete_cinema, name='cinema_delete'),
    path('ajax/delete-hall/<int:pk>/', views.api_delete_hall, name='hall_delete'),
    path('ajax/delete-news/<int:pk>/', views.api_delete_news_object, name='news_delete'),
    path('ajax/delete-stock/<int:pk>/', views.api_delete_stock, name='stock_delete'),
    path('ajax/delete-user/<str:email>/', views.api_delete_user, name='user_delete'),
    path('ajax/delete-html-email/<int:pk>/', views.api_delete_html_email, name='html_email_delete'),
    path('ajax/api-update-ticket/<int:pk>/', views.api_update_session_ticket, name='ticket_update'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('movies/update-movie-info/<int:pk>/', views.update_movie_info, name='movie_update'),
    path('movies/add-movie/', views.movie_create, name='movie_add'),
    path('movies/', staff_member_required(views.MovieListView.as_view(), login_url=reverse_lazy('admin:login')), name='movies'),
    path('cinemas/update-cinema-info/<int:pk>/', views.update_cinema_info, name='cinema_update'),
    path('cinemas/add-cinema/', views.cinema_create, name='cinema_add'),
    path('cinemas/<int:cinema_pk>/add-hall/', views.hall_create, name='add_hall_to_cinema'),
    path('cinemas/<int:cinema_pk>/update-hall-info/<int:pk>/', views.update_hall_info, name='hall_update'),
    path('cinemas/', staff_member_required(views.CinemaListView.as_view(), login_url=reverse_lazy('admin:login')), name='cinemas'),
    path('sessions/add-session/', views.session_create, name='session_add'),
    path('sessions/update-session-info/<int:pk>/', views.update_session_info, name='session_update'),
    path('sessions/', staff_member_required(views.SessionListView.as_view(), login_url=reverse_lazy('admin:login')), name='sessions'),
    path('news/add-news/', views.news_create, name='news_add'),
    path('news/update-news-info/<int:pk>/', views.update_news_info, name='news_update'),
    path('news/', staff_member_required(views.NewsListView.as_view(), login_url=reverse_lazy('admin:login')), name='news'),
    path('stocks/add-stock/', views.stock_create, name='stock_add'),
    path('stocks/update-stock-info/<int:pk>/', views.update_stock_info, name='stock_update'),
    path('stocks/', staff_member_required(views.StockListView.as_view(), login_url=reverse_lazy('admin:login')), name='stocks'),
    path('main-page/', views.main_page, name='main_page'),
    path('cafe-bar-page/', views.cafe_bar_page, name='cafe_bar_page'),
    path('vip-hall-page/', views.vip_hall_page, name='vip_hall_page'),
    path('about-cinema-page/', views.about_cinema_page, name='about_cinema_page'),
    path('advertise-page/', views.advertise_page, name='advertise_page'),
    path('children-room-page/', views.children_room_page, name='children_room_page'),
    path('mobile-app-page/', views.mobile_app_page, name='mobile_app_page'),
    path('cinema-contacts/', views.contacts_page, name='cinema_contacts'),
    path('main-page-banners/', views.main_page_banners, name='main_page_banners'),
    path('news-and-stocks-page-banners/', views.news_and_stocks_banners, name='news_and_stocks_page_banners'),
    path('users/update-user-info/<str:email>/', views.change_user_info, name='user_update'),
    path('users/', staff_member_required(views.UserListView.as_view(), login_url=reverse_lazy('admin:login')), name='users'),
    path('mailing/', views.mailing, name='mailing'),
    path('', views.index, name='index'),
]
