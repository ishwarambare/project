from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from blog.forms import UserForm, PostForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import authenticate
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from blog.models import Post
from django.contrib.auth.models import User
from django.shortcuts import render
from .filters import PostFilter


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
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('blog:home')
        else:
            # return HttpResponseRedirect(reverse('blog:home')
            # form = PostForm()
            return redirect('blog:home')
            # return render(request, 'list.html.j2', {'form': form})
    else:
        return render(request, 'list.html.j2')


def home(request):
    post = Post.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(post, 2)
    form = PostForm()
    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)
    return render(request, 'list.html.j2', {'post': post, 'page': page, 'form': form})


def search(request):
    user_list = Post.objects.all()
    user_filter = PostFilter(request.GET, queryset=user_list)
    return render(request, 'search_list.html.j2', {'filter': user_filter})
