from rest_framework import serializers
from . import models


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'body', 'created_time', 'modified_time', 'excerpt', 'category', 'tag', 'author', 'views')
        model = models.Post
