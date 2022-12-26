from . import views
from django.urls import path

urlpatterns = [
    path('', views.class_list, name='classes'),
    path('book/', views.book, name='book'),
    path('reservations/', views.reservations, name='reservations'),
    path('delete/<reservation_id>', views.delete_reservation, name='delete'),
    path('delete/note/<note_id>', views.delete_note, name='delete_note'),
    path('edit/note/<note_id>', views.edit_note, name='edit_note'),
]
