from django.test import TestCase
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import User, YogaType, YogaClass, Reservation, Notes


class TestViews(TestCase):

    def setUp(self):
        username = "Marla"
        password = "Django123"
        self.user = get_user_model().objects.create_user(
            username=username,
            password=password
        )
        login = self.client.login(username=username, password=password)
        self.assertTrue(login)

        self.yoga_type_test = YogaType.objects.create(
            title="test_type", status="1")

        self.yoga_class = YogaClass.objects.create(
            yoga_type=self.yoga_type_test, status="1")

        self.reservation = Reservation.objects.create(
            yoga_class=self.yoga_class, member=self.user, approved="True")

        self.note = Notes.objects.create(
            reservation=self.reservation)

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_about(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')

    def test_info(self):
        response = self.client.get('/info/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'info.html')

    def test_class_list(self):
        response = self.client.get('/classes/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/classes.html')

    def test_reservations(self):
        response = self.client.get('/classes/reservations/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/reservations.html')

    def test_delete_reservation(self):
        reservation = self.reservation
        response = self.client.get(f'/classes/delete/{reservation.id}')
        self.assertRedirects(response, '/classes/reservations/')
        existing_reservation = Reservation.objects.filter(id=reservation.id)
        self.assertEquals(len(existing_reservation), 0)

    def test_book(self):
        response = self.client.get('/classes/book/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/book_class.html')

    def test_edit_note(self):
        note = self.note
        response = self.client.get(f'/classes/edit/note/{note.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/edit_note.html')

    def test_delete_note(self):
        note = self.note
        response = self.client.get(f'/classes/delete/note/{note.id}')
        self.assertRedirects(response, '/classes/reservations/')
        existing_note = Notes.objects.filter(id=note.id)
        self.assertEquals(len(existing_note), 0)
