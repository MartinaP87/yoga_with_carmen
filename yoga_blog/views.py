from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Post
from .forms import CommentForm


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
    comments = post.comments.filter(approved=True).order_by("-created_on")
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        liked = True
    commented = False
    comment_form = CommentForm()
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(
                request, 'You successfully left a comment.<br>\
                Your comment is waiting for approval.')
            commented = True
        else:
            comment_form = CommentForm()
    comment_form = CommentForm()
    context = {
                "post": post,
                "comments": comments,
                "commented": commented,
                "liked": liked,
                "comment_form": comment_form,
            }
    return render(request, "yoga_blog/post_detail.html", context)


def post_like(request, slug):
    """
    It toggles likes; It removes the like if it already
    exists or adds the like if previously not applied.
    """
    post = get_object_or_404(Post, slug=slug)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('post_detail', slug)
