# from allauth.account.forms import SignupForm
from django import forms

from django.http import HttpResponseForbidden
from .models import MPTTComment, Post, User
from django_comments.forms import CommentForm
from django_summernote.widgets import SummernoteInplaceWidget, SummernoteWidget


class MySignupForm(forms.Form):
    avatar = forms.ImageField(label='头像', allow_empty_file=True)

    def signup(self, request, user):
        form = MySignupForm(request.POST, request.FILES)
        if form.is_valid():
            user.avatar = form.cleaned_data['avatar']
            user.save()
        else:
            return HttpResponseForbidden('not allowed')


class MPTTCommentForm(CommentForm):
    parent = forms.ModelChoiceField(queryset=MPTTComment.objects.all(), required=False)
    comment = forms.CharField(widget=SummernoteWidget())

    def get_comment_create_data(self, site_id=None):
        data = super(MPTTCommentForm, self).get_comment_create_data()
        data['parent'] = self.cleaned_data['parent']
        return data


class PostForm(forms.ModelForm):
    # title = forms.CharField(label='标题', max_length=50)
    # body = forms.CharField(label='正文', widget=forms.Textarea)
    # category = forms.ModelChoiceField(label='分类', queryset=Category.objects.all())
    class Meta:
        model = Post
        fields = ['title', 'body', 'category']
        widgets = {
            'body': SummernoteWidget()
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname', 'signature', 'avatar']


