from django.contrib import admin
from django.urls import path, include
from bookings import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home_page, name='home'),
    path("about/", views.about, name="about"),
    path("info/", views.info, name="info"),
    path("classes/", include("bookings.urls"), name="bookings-urls"),
    path("blog/", include("yoga_blog.urls"), name="yoga_blog-urls"),
    path('summernote/', include('django_summernote.urls')),
    path("accounts/", include("allauth.urls")),
]
