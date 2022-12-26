from django.shortcuts import render, get_object_or_404, redirect
from .models import User, YogaType, YogaClass, Reservation, Notes


def home_page(request):
    """
    It renders the home page and today's class.
    """
    todays_class = YogaClass.objects.filter(status=1, day=date.today())
    context = {
        'todays_class': todays_class
    }
    return render(request, "index.html", context)


def about(request):
    """
    It renders the about page.
    """
    return render(request, "about.html")


def class_list(request):
    """
    It renders classes and passes the class list to the template.
    """
    yoga_types_list = YogaType.objects.filter(status=1)
    context = {
        'yoga_types_list': yoga_types_list
    }
    return render(request, "bookings/classes.html", context)


def info(request):
    """
    It renders the info page.
    """
    return render(request, "info.html")