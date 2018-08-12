from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import mark_safe
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill
from django_comments.abstracts import CommentAbstractModel
from mptt.models import MPTTModel, TreeForeignKey
from django.utils import timezone
from django.urls import reverse
from markdown import markdown


# comment
class MPTTComment(MPTTModel, CommentAbstractModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        # comments on one level will be ordered by date of creation
        order_insertion_by = ['submit_date']
    #
    # class Meta:
    #     ordering = ['tree_id', 'lft']


# User
class User(AbstractUser):
    nickname = models.CharField('昵称', max_length=50, blank=True)
    signature = models.TextField('签名', max_length=500, blank=True)
    avatar = models.ImageField('头像', upload_to='avatar', blank=True)
    thumbnail = ProcessedImageField(upload_to='avatar',
                                    blank=True,
                                    processors=[ResizeToFill(360, 360)],
                                    format='JPEG',
                                    options={'quality': 60})

    avatar_thumbnail = ImageSpecField(source='avatar',
                                      processors=[ResizeToFill(100, 100)],
                                      format='JPEG',
                                      options={'quality': 60})

    avatar_thumbnail_big = ImageSpecField(source='avatar',
                                          processors=[ResizeToFill(215, 215)],
                                          format='JPEG',
                                          options={'quality': 60})

    class Meta(AbstractUser.Meta):
        pass


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField('标题', max_length=70)
    body = models.TextField(max_length=70000, verbose_name='正文')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    modified_time = models.DateTimeField('修改时间', auto_now=True)
    excerpt = models.CharField('摘要', max_length=200, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='类别')
    tag = models.ManyToManyField(Tag, blank=True, verbose_name='标签')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    views = models.PositiveIntegerField('阅读数', default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail', kwargs={'post_id': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def get_body_as_markdown(self):
        return mark_safe(markdown(self.body, safe_mode='escape'))

##Forum

