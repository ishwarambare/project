from django import forms
from django.contrib.auth.models import User

from blog.models import Post


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
