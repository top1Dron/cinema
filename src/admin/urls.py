from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path, reverse_lazy

from admin import views


app_name = 'admin'


urlpatterns = [
    path('ajax/delete-image/<int:pk>/', views.api_delete_image, name='delete_image'),
    path('ajax/delete-movie/<int:pk>/', views.api_delete_movie, name='movie_delete'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('movies/update-movie-info/<int:pk>/', views.update_movie_info, name='movie_update'),
    path('movies/add-movie/', views.movie_create, name='movie_add'),
    path('movies/', staff_member_required(views.MovieListView.as_view(), login_url=reverse_lazy('admin:login')), name='movies'),
    path('', views.index, name='index'),
]
