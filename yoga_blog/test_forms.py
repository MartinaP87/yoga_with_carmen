from django.test import TestCase
from .forms import CommentForm


class TestCommentForm(TestCase):

    def test_body_is_required(self):
        comment_form = CommentForm({"body": ""})
        self.assertFalse(comment_form.is_valid())
        self.assertIn("body", comment_form.errors.keys())
        self.assertEqual(
            comment_form.errors["body"][0], "This field is required.")

    def test_fields_are_explicit_in_comment_form_metaclass(self):
        comment_form = CommentForm()
        self.assertEqual(comment_form.Meta.fields, ('body',))
