from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Post, MPTTComment, User
from django.core.paginator import Paginator
from .forms import PostForm
from django.utils import timezone
import markdown


def index(request):
    latest_post_list = Post.objects.order_by('created_time')[:2]
    post_list = Post.objects.order_by('created_time')[2:]
    paginator = Paginator(post_list, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context = {'latest_post_list': latest_post_list,
               'posts': posts}
    return render(request, 'blog/index.html', context)


def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comment_list = MPTTComment.objects.all()
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    context = {'post': post,
               'comment_list': comment_list}
    return render(request, 'blog/blog-single.html', context)


def reply(request, comment_id):
    comment = get_object_or_404(MPTTComment, pk=comment_id)
    post = get_object_or_404(Post, pk=comment.object_pk)
    context = {'comment': comment,
               'post': post}
    return render(request, 'blog/comment.html', context)


def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    context = {'user': user}
    return render(request, 'blog/profile.html', context)


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            category = form.cleaned_data['category']
            user = request.user
            if user.is_authenticated:
                post = Post(title=title, body=body, category=category, author=user)
                post.save()
                return HttpResponseRedirect(reverse('detail', args=[post.id]))
            else:
                return HttpResponse('请先登录')
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})


def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post.title = form.cleaned_data['title']
            post.body = form.cleaned_data['body']
            post.category = form.cleaned_data['category']
            user = request.user
            if user.is_authenticated:
                post.save()
                return HttpResponseRedirect(reverse('detail', args=[post.id]))
            else:
                return HttpResponse('请先登录')
    else:
        form = PostForm(initial={'body': post.body, 'title': post.title, 'category': post.category})
    return render(request, 'blog/edit_post.html', {'form': form})
