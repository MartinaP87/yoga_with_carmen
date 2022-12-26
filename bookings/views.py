from django.shortcuts import render, get_object_or_404, redirect
from .models import User, YogaType, YogaClass, Reservation, Notes
from django.contrib import messages
from .forms import ReservationForm, NotesForm
from datetime import date, timedelta


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


def reservations(request):
    """
    It renders reservations and passes the
    reservations to the template.
    It renders Notes form and handles
    validation to create a new note.
    It passes all notes to the template.
    """
    reservations = Reservation.objects.all()
    context = {
        'reservations': reservations
    }
    return render(request, 'bookings/reservations.html', context)


def book(request):
    """
    It renders book_class and passes classes to the template.
    It passes days and time_slots to the
    template to create and update the calendar.
    It renders the Reservation form and handles validation.
    """
    time_slots = ["9:00 - 10:00", "10:00 - 11:00",
                  "11:00 - 12:00", "14:00 - 15:00",
                  "15:00 - 16:00", "16:00 - 17:00",
                  "17:00 - 18:00", "20:00 - 21:00"]
    week_days = get_days(request)
    yoga_classes = no_obsolete_classes(request)
    yoga_classes_available = yoga_classes_available_now(request)
    """
    If the method is post, it saves the form.
    """
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.instance.member_id = request.user.id
            new_reservation = form.save()
            valid_reservation(
                request, new_reservation, yoga_classes_available)
    form = ReservationForm()
    context = {
        'time_slots': time_slots,
        'week_days': week_days,
        'yoga_classes': yoga_classes,
        'form': form
    }
    return render(request, 'bookings/book_class.html', context)


def get_days(request):
    """
    It sets the timeframe for the calendar and
    the classes that will be displayed.
    """
    today = date.today()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=13)
    dates = [start + timedelta(days=i) for i in range((end-start).days+1)]
    return (dates)


def no_obsolete_classes(request):
    """
    It deletes classes from the week before the current one.
    """
    week_days = get_days(request)
    yoga_classes = YogaClass.objects.filter(status=1)
    if yoga_classes:
        for yoga_class in yoga_classes:
            if yoga_class.day < week_days[0]:
                yoga_class.delete()
                return redirect('book')
    return yoga_classes


def yoga_classes_available_now(request):
    """
    It allows classes to be accessible only if not older than today.
    """
    yoga_classes = no_obsolete_classes(request)
    yoga_classes_available = []
    for yoga_class in yoga_classes:
        if yoga_class.day >= date.today():
            yoga_classes_available.append(yoga_class)
    return yoga_classes_available


def valid_reservation(request, reservation, bookable_classes):
    """
    Checks if the new reservation is in the correct timeframe,
    otherwise it displays a message and deletes reservation.
    """
    if reservation.yoga_class in bookable_classes:
        check_double_booking(request, reservation.id)
    else:
        messages.error(request, "This class is not longer available")
        reservation.delete()


def check_double_booking(request, reservation_id):
    """
    It checks if the user already has a reservation
    for the same class; if so, it deletes the
    reservation and displays a  message.
    """
    reservation = get_object_or_404(Reservation, id=reservation_id)
    current_user = request.user
    yoga_class_user_reservations = Reservation.objects.filter(
        yoga_class_id=reservation.yoga_class_id, member=current_user)
    if yoga_class_user_reservations.count() > 1:
        messages.error(
                request, "You are already booked \
                    in for this class!")
        reservation.delete()
    else:
        reserved_class_id = reservation.yoga_class_id
        updated_reservation = update_approval(
                        request, reservation.id)
        fully_booked(request, updated_reservation.id)


def update_approval(request, reservation_id):
    """
    It checks if the class has available spaces;
    if so, it saves the reservation as approved
    otherwise, the reservation's approved status is
    set to False.
    """
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reserved_class_id = reservation.yoga_class_id
    queryset = YogaClass.objects.filter(status=1)
    chosen_yoga_class = get_object_or_404(queryset, id=reserved_class_id)
    if chosen_yoga_class.available_spaces > 0:
        reservation.approved
        reservation.save()
    else:
        reservation.approved = False
        reservation.save()
    return reservation


def fully_booked(request, reservation_id):
    """
    It checks if the class is approved;
    if so, it calls reduce_available_spaces function;
    otherwise, it deletes the reservation and displays
    a message.
    """
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if reservation.approved:
        messages.success(
            request, 'Your booking was successful!')
        reduce_available_spaces(
            request, reservation.yoga_class_id)
    else:
        messages.error(
            request, 'Unfortunately the class is \
fully booked, choose another class!')
        reservation.delete()


def reduce_available_spaces(request, chosen_class_id):
    """
    It reduces by one the number of available spaces in a yoga class
    every time it's called.
    """
    queryset = YogaClass.objects.filter(status=1)
    chosen_yoga_class = get_object_or_404(queryset, id=chosen_class_id)
    spaces = int(chosen_yoga_class.available_spaces)
    updated_spaces = spaces - 1
    chosen_yoga_class.available_spaces = updated_spaces
    chosen_yoga_class.save()
