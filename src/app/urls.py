from django.urls import path
from app import views


app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('cafe-bar/', views.cafe_bar_page, name='cafe_bar_page'),
    path('advertise/', views.advertise_page, name="advertise_page"),
    path('about-cinema/', views.about_cinema, name="about_cinema"),
    path('mobile-app/', views.mobile_app_page, name="mobile_app_page"),
    path('children-room/', views.children_room_page, name="children_room_page"),
    path('contacts/', views.contacts_page, name="contacts_page"),
    path('news/<int:pk>', views.NewsDetailView.as_view(), name="news_detail"),
    path('news/', views.news_list, name="news"),
    path('stocks/<int:pk>', views.StockDetailView.as_view(), name="stock_detail"),
    path('stocks/', views.stocks_list, name="stocks"),
    path('sign-up/', views.signup, name="signup"),
    path('profile/', views.profile, name="profile"),
    path('logout/', views.logout_user, name="logout"),
    path('login/', views.login, name="login"),
    path('cinemas/<int:pk>', views.cinema_detail, name="cinema_detail"),
    path('cinemas/', views.cinemas_list, name="cinema_list"),
    path('hall/<int:pk>', views.hall_detail, name="hall_detail"),
    path('afiche/', views.afiche, name="afiche"),
    path('soon/', views.soon, name="soon"),
    path('movie/<int:pk>/', views.movie_detail, name="movie_detail"),
    path('movie/find-movies/', views.find_movie, name='find_movie'),
    path('shedule/', views.SheduleListView.as_view(), name="shedule"),
    path('shedule/book-tickets/<int:pk>/', views.book_tickets_for_session, name="book_tickets_for_session"),
    path('shedule/buy-tickets/<int:pk>/', views.buy_tickets_for_session, name="buy_tickets_for_session"),
    path('tickets/', views.view_user_tickets, name='view_user_tickets'),
    path('return-ticket/<int:pk>/', views.return_a_ticket, name='return_a_ticket'),
    path('buy-ticket/<int:pk>/', views.buy_the_ticket, name='buy_the_ticket'),
]
