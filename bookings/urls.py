from . import views
from django.urls import path

urlpatterns = [
    path('', views.class_list, name='classes'),
]