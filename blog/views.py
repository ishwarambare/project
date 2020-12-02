from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from blog.forms import UserForm, PostForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import authenticate

from blog.models import Post


def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponse('login sucessfull')
        else:
            return HttpResponse('please check the credential')
    else:
        form = UserForm()
        return render(request, 'signup.html.j2', {'form': form})


def login_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
        else:
            messages.error(request, "Invalid username or password.")
            return HttpResponse("please check your credential")
    else:
        return render(request, 'login.html.j2', {'form': form})


def main(request):
    return HttpResponse('home function')


def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("blog:home")


def post_view_form(request):
    if request.method == 'POST':
        pass
    else:
        form = PostForm()
        return render(request, 'form.html.j2', {'form': form})


def home(request):
    post = Post.objects.all()
    return render(request,'list.html.j2',{'post':post})
