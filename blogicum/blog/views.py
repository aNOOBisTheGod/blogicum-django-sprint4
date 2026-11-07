"""Publications, profiles and author-controlled editing."""
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import CommentForm, PostForm, ProfileForm
from .models import Category, Comment, Post

POSTS_PER_PAGE = 10


def posts_queryset(visible=True):
    """Load related objects and comment counts with the publications."""
    posts = Post.objects.select_related('author', 'category', 'location')
    if visible:
        posts = posts.filter(is_published=True,
                             category__is_published=True,
                             pub_date__lte=timezone.now())
    return posts.annotate(comment_count=Count('comments')).order_by(
        '-pub_date', '-pk',
    )


def page(request, posts):
    """Return a robust page for the requested page number."""
    return Paginator(posts, POSTS_PER_PAGE).get_page(request.GET.get('page'))


def index(request):
    """Display recent public posts."""
    return render(request, 'blog/index.html', {
        'page_obj': page(request, posts_queryset()),
    })


def category_posts(request, category_slug):
    """Display visible publications in a published category."""
    category = get_object_or_404(Category, slug=category_slug,
                                 is_published=True)
    return render(request, 'blog/category.html', {
        'category': category,
        'page_obj': page(request, posts_queryset().filter(category=category)),
    })


def profile(request, username):
    """Authors can see all their own publications."""
    author = get_object_or_404(get_user_model(), username=username)
    posts = posts_queryset(
        visible=request.user != author,
    ).filter(author=author)
    return render(request, 'blog/profile.html', {
        'profile': author, 'page_obj': page(request, posts),
    })


def post_detail(request, post_id):
    """Allow the author to preview unpublished posts."""
    post = get_object_or_404(posts_queryset(False), pk=post_id)
    if request.user != post.author:
        post = get_object_or_404(posts_queryset(), pk=post_id)
    return render(request, 'blog/detail.html', {
        'post': post, 'form': CommentForm(),
        'comments': post.comments.select_related('author').all(),
    })


@login_required
def create_post(request):
    """Create a post belonging to the authenticated author."""
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/create.html', {'form': form})


@login_required
def edit_post(request, post_id):
    """Only the author may edit a publication."""
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return redirect('blog:post_detail', post_id=post.pk)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post.pk)
    return render(request, 'blog/create.html', {'form': form})


@login_required
def delete_post(request, post_id):
    """Require confirmation before deleting an author's publication."""
    post = get_object_or_404(Post, pk=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/create.html', {
        'form': PostForm(instance=post),
    })


@login_required
def edit_profile(request):
    """Edit only the authenticated user's profile."""
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        return redirect('blog:profile', username=user.username)
    return render(request, 'blog/user.html', {'form': form})


@login_required
def add_comment(request, post_id):
    """Attach a validated comment to a visible publication."""
    post = get_object_or_404(posts_queryset(), pk=post_id)
    form = CommentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', post_id=post.pk)


@login_required
def edit_comment(request, post_id, comment_id):
    """Only its author may edit a comment."""
    comment = get_object_or_404(Comment, pk=comment_id, post_id=post_id,
                                author=request.user)
    form = CommentForm(request.POST or None, instance=comment)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/comment.html', {
        'form': form, 'comment': comment,
    })


@login_required
def delete_comment(request, post_id, comment_id):
    """Require confirmation before removing an author's comment."""
    comment = get_object_or_404(Comment, pk=comment_id, post_id=post_id,
                                author=request.user)
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/comment.html', {'comment': comment})
