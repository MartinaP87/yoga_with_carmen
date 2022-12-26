from django.contrib import admin
from .models import YogaType, YogaClass, Reservation
from django_summernote.admin import SummernoteModelAdmin


@admin.register(YogaType)
class YogaTypeAdmin(SummernoteModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'title')
    list_display = ('title', 'status')
    search_fields = ['title', 'description']
    summernote_fields = ('description')


@admin.register(YogaClass)
class YogaClassAdmin(SummernoteModelAdmin):

    list_filter = ('status', 'yoga_type')
    list_display = ('yoga_type', 'day', 'time', 'status', 'available_spaces')
    search_fields = ['yoga_type', 'day']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_filter = ('yoga_class', 'approved',)
    list_display = ('yoga_class', 'member', 'approved')
    search_fields = [
        'member', 'yoga_class']
    actions = ['approve']

    def approve(self, request, queryset):
        queryset.update(approved=True)
