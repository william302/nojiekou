from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from blog.models import Post, MPTTComment, User
import markdown


def index(request):
    latest_post_list = Post.objects.order_by('created_time')[:2]
    context = {'latest_post_list': latest_post_list}
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
