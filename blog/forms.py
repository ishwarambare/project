from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from blog.models import Post


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if not authenticate(username=username, password=password):
            raise forms.ValidationError("Wrong login or password")
        return self.cleaned_data


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # fields = '__all__'
        fields = ['name', 'category', 'description', 'image', 'is_active']

    def clean_name(self):
        cd = self.cleaned_data
        num = len(cd['name'])
        exists = Post.objects.filter(name__icontains=cd["name"]).exists()
        if cd["name"] == '' or num > 10 or exists:
            raise forms.ValidationError('Please fill some thing here under 10 car same post ')
        return cd['name']

    def clean_category(self):
        cd = self.cleaned_data
        if cd['category'] == '':
            raise forms.ValidationError('Please fill some thing here')
        return cd['name']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
