from django.test import TestCase
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Post, Comment
from datetime import date, timedelta


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
        self.post = Post.objects.create(
            title='TestPostToComment', author=self.user, slug='test_slug',
            status=1)

    def test_blog(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yoga_blog/blog.html')

    def test_post_detail(self):
        post = self.post
        response = self.client.get(f'/blog/{post.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'yoga_blog/post_detail.html')

    def test_post_like2(self):
        post = self.post
        response = self.client.get(f'/blog/like/{post.slug}')
        self.assertEqual(response.status_code, 302)
