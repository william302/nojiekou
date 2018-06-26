from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Post, Tag, Category, User, MPTTComment
from mptt.admin import MPTTModelAdmin
# Register your models here.


admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(MPTTComment, MPTTModelAdmin)
