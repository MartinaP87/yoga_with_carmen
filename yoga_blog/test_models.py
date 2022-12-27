from django.contrib.auth.models import User
from django.test import TestCase
from .models import Post, Comment


class TestModels(TestCase):

    def test_post_status_delfault_zero(self):
        user = User.objects.create(username='TestUsername')
        post = Post.objects.create(title='TestPost', author=user)
        self.assertEqual(post.status, 0)

    def test_comment_approved_default_false(self):
        user = User.objects.create(username='TestUsernameComment')
        post = Post.objects.create(title='TestPostToComment', author=user)
        comment = Comment.objects.create(name='TestComment', post=post)
        self.assertFalse(comment.approved)
