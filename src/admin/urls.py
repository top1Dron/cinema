from django.urls import path

from admin import views


app_name = 'admin'


urlpatterns = [
    path('', views.index, name='index'),
    path('ajax/delete-image/<int:pk>/', views.api_delete_image, name='delete_image'),
    path('movies/add-movie/', views.movie_create, name='movie_add'),
    path('movies/update-movie-info/<int:pk>/', views.update_movie_info, name='movie_update'),
]
