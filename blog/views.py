from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Post, MPTTComment, User, Category
from django.core.paginator import Paginator
from .forms import PostForm, UserForm
from django.utils import timezone
import markdown


def index(request):
    latest_post_list = Post.objects.order_by('created_time')[:5]
    post_list = Post.objects.order_by('created_time')[5:]
    paginator = Paginator(post_list, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context = {'latest_post_list': latest_post_list,
               'posts': posts}
    return render(request, 'blog/index.html', context)


def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    latest_post_list = Post.objects.all().order_by('-created_time')[:2]
    post.increase_views()
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    context = {'post': post,
               'latest_post_list': latest_post_list}
    return render(request, 'blog/blog-single.html', context)


def reply(request, comment_id):
    comment = get_object_or_404(MPTTComment, pk=comment_id)
    post = get_object_or_404(Post, pk=comment.object_pk)
    context = {'comment': comment,
               'post': post}
    return render(request, 'blog/comment.html', context)


def profile(request, user_id):
    profile_user = get_object_or_404(User, pk=user_id)
    posts = Post.objects.all().filter(author=profile_user)
    context = {'profile_user': profile_user,
               'posts': posts}
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form = UserForm(request.POST, request.FILES, instance=profile_user)
            form.save()
            return redirect('profile', user_id=profile_user.id)
    else:
        form = UserForm(instance=profile_user)
    context.update({'form': form})
    return render(request, 'blog/profile.html', context)


@login_required
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


@login_required()
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # post.title = form.cleaned_data['title']
            # post.body = form.cleaned_data['body']
            # post.category = form.cleaned_data['category']
            form = PostForm(request.POST, instance=post)
            form.save()
            return HttpResponseRedirect(reverse('detail', args=[post.id]))
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/edit_post.html', {'form': form, 'post':post})


def posts(request):
    category_list = Category.objects.all()
    post_list = Post.objects.all()
    latest_post_list = Post.objects.order_by('-created_time')[:3]
    context = {'post_list': post_list,
               'category_list': category_list,
               'latest_post_list': latest_post_list}
    return render(request, 'blog/posts.html', context)


def category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    post_list = Post.objects.filter(category=category)
    latest_post_list = Post.objects.order_by('-created_time')[:3]
    context = {'post_list': post_list,
               'category': category,
               'latest_post_list': latest_post_list}
    return render(request, 'blog/category.html', context)
