from django import template
from ..models import Post, Category


register = template.Library()


@register.simple_tag
def get_recent_posts(num=3):
    return Post.objects.all().order_by('-created_time')[:num]


@register.simple_tag
def get_categories():
    return Category.objects.all()
