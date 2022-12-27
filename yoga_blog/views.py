from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Post


def post_list(request):
    """
    It renders about page and passes the post list to the template.
    It paginates the blog posts.
    """
    post_list = Post.objects.filter(status=1).order_by("-created_on")
    paginator = Paginator(post_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'post_list': post_list,
        'page_obj': page_obj
    }
    return render(request, "yoga_blog/blog.html", context)


def post_detail(request, slug):
    """
    It renders post detail and passes posts, comments,
    comment form, and likes to the template.
    Handles comment form validation and sends a message
    to the user when the form is submitted successfully.
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    context = {
                "post": post,
            }
    return render(request, "yoga_blog/post_detail.html", context)
