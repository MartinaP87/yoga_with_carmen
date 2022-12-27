from django.contrib.auth.models import User
from django.test import TestCase
from .models import YogaType, YogaClass, Reservation, Notes


class TestModels(TestCase):

    def test_yoga_type_status_default_to_zero(self):
        yoga_type = YogaType.objects.create(title="TestYogaType")
        self.assertEqual(yoga_type.status, 0)

    def test_yoga_type_introduction_default_to_intro(self):
        yoga_type = YogaType.objects.create(title="TestYogaType")
        self.assertEqual(yoga_type.introduction, "intro")

    def test_yoga_class_time_default_nine_to_ten(self):
        yoga_type_test = YogaType.objects.create(title="TestYogaType")
        yoga_class = YogaClass.objects.create(yoga_type=yoga_type_test)
        self.assertEqual(yoga_class.time, "9:00 - 10:00")

    def test_yoga_class_available_spaces_default_twenty(self):
        yoga_type_test = YogaType.objects.create(title="TestYogaType")
        yoga_class = YogaClass.objects.create(yoga_type=yoga_type_test)
        self.assertEqual(yoga_class.available_spaces, 20)

    def test_yoga_class_status_default_zero(self):
        yoga_type_test = YogaType.objects.create(title="TestYogaType")
        yoga_class = YogaClass.objects.create(yoga_type=yoga_type_test)
        self.assertEqual(yoga_class.status, 0)

    def test_reservation_approved_default_true(self):
        yoga_type_test = YogaType.objects.create(title="TestYogaType")
        yoga_class = YogaClass.objects.create(yoga_type=yoga_type_test)
        user = User.objects.create(username='TestUsernameCooment')
        reservation = Reservation.objects.create(
            yoga_class=yoga_class, member=user)
        self.assertTrue(reservation.approved)

    def test_notes_annotation_default_remember(self):
        yoga_type_test = YogaType.objects.create(title="TestYogaType")
        yoga_class = YogaClass.objects.create(yoga_type=yoga_type_test)
        user = User.objects.create(username='TestUsernameCooment')
        reservation = Reservation.objects.create(
            yoga_class=yoga_class, member=user)
        note = Notes.objects.create(reservation=reservation)
        self.assertEqual(note.annotation, "Remember...")
