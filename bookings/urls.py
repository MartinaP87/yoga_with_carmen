from . import views
from django.urls import path

urlpatterns = [
    path('', views.class_list, name='classes'),
    path('book/', views.book, name='book'),
    path('reservations/', views.reservations, name='reservations'),
]
