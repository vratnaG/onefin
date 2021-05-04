from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegsiterView.as_view(), name='register'),
    path('movies/', views.movies_list, name='movie_list'),
    path('collection/', views.collection_list,
         name='collection_list_or_collection_add'),
    path('collection/<str:uuid>', views.collection_detail,
         name='collection_detail'),
]
