from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Post, Tag, Category, User, MPTTComment
from mptt.admin import MPTTModelAdmin
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.


class PostModelAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'

admin.site.register(Post, PostModelAdmin)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(MPTTComment, MPTTModelAdmin)
