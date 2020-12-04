from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import RedirectView

from blog.forms import UserForm, PostForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import authenticate
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from blog.models import Post, Category, Like
from django.contrib.auth.models import User
from django.shortcuts import render
from .filters import PostFilter
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm

from django.contrib.auth.forms import UserCreationForm

# def signup(request):
#     if request.method == 'POST':
#         # form = UserForm(request.POST)
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             print(user)
#             # user.set_password(user.password)
#             user.save()
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             login(request, user)
#             return redirect('blog:login')
#         else:
#             return HttpResponse('please check the credential')
#     else:
#         # form = UserForm()
#         creation_form = UserCreationForm()
#         return render(request, 'signup.html.j2', {'form': creation_form})


from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('blog:login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html.j2', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username_ = data['username']
            print(username_)
            password_ = data['password']
            print(password_)
            user = authenticate(request, username=username_, password=password_)
            print(user)
            if user is None:
                print(user)
                login(request, user)
                return redirect('blog:home')
            else:
                return HttpResponse('Disabled account')

        # form = AuthenticationForm(request=request, data=request.POST)
        # if form.is_valid():
        #     username = form.cleaned_data.get('username')
        #     password = form.cleaned_data.get('password')
        #     user = authenticate(username=username, password=password)
        #     if user is not None:
        #         login(request, user)
        #         messages.info(request, f"You are now logged in as {username}")
        #         return redirect('blog:home')

        else:
            messages.error(request, "Invalid username or password.")
            return HttpResponse("please check your credential")
    else:
        form = LoginForm()
        return render(request, 'login.html.j2', {'form': form})


def main(request):
    return HttpResponse('home function')


def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("blog:login")


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

    cat = Category.objects.all()
    return render(request, 'list.html.j2', {'post': post,
                                            'page': page,
                                            'form': form,
                                            'cat': cat,
                                            # "likes": Like.objects.all(),
                                            })


# def search(request):
#     user_list = Post.objects.all()
#     user_filter = PostFilter(request.GET, queryset=user_list)
#     return render(request, 'search_list.html.j2', {'filter': user_filter})


def search(request):
    if request.method == 'GET':
        search_name = request.GET.get('search')
        status = Post.objects.filter(Q(name__icontains=search_name) | Q(description__icontains=search_name))
        return render(request, "search_list.html.j2", {"books": status})
    else:
        return HttpResponse('search not found')


@login_required
def categories(request, pk):
    cat = Post.objects.filter(category_id=pk)
    return render(request, 'base.html.j2', {'cat': cat})


def like(request, post_id):
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        post = Post.objects.get(id=post_id)
        newLike = Like(user=user, post=post)
        newLike.alreadyLiked = True

        post.likes += 1
        post.user_likes.add(user)
        post.save()
        newLike.save()
        return HttpResponseRedirect(reverse('blog:home'))


# @login_required
# def like(request, postid, userpreference):
#     if request.method == "POST":
#         eachpost = get_object_or_404(Post, id=postid)
#         obj = ''
#         valueobj = ''
#         try:
#             obj = Like.objects.get(user=request.user, post=eachpost)
#             valueobj = obj.value  # value of userpreference
#             valueobj = int(valueobj)
#             userpreference = int(userpreference)
#             if valueobj != userpreference:
#                 obj.delete()
#                 upref = Like()
#                 upref.user = request.user
#                 upref.post = eachpost
#                 upref.value = userpreference
#                 if userpreference == 1 and valueobj != 1:
#                     eachpost.likes += 1
#                 upref.save()
#                 eachpost.save()
#                 context = {'eachpost': eachpost,
#                            'postid': postid}
#                 return render(request, 'list.html.j2', context)
#             elif valueobj == userpreference:
#                 obj.delete()
#
#                 if userpreference == 1:
#                     eachpost.likes -= 1
#
#                     eachpost.save()
#
#                 context = {
#                     'eachpost': eachpost,
#                     'postid': postid,
#                     }
#                 return render(request, 'list.html.j2', context)
#         except:
#             upref = Like()
#             upref.user = request.user
#             upref.post = eachpost
#             upref.value = userpreference
#             userpreference = int(userpreference)
#             if userpreference == 1:
#                 eachpost.likes += 1
#             upref.save()
#             eachpost.save()
#             context = {'eachpost': eachpost,
#                        'postid': postid}
#             return render(request, 'list.html.j2', context)
#     else:
#         eachpost = get_object_or_404(Post, id=postid)
#         context = {'eachpost': eachpost,
#                    'postid': postid}
#         return render(request, 'list.html.j2', context)


# from common.decorators import ajax_required
from django.http import HttpResponseBadRequest


def ajax_required(f):
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Post.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'error'})


class PostLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        print(pk)
        obj = get_object_or_404(Post, pk=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.user_likes.all():
                obj.user_likes.remove(user)
                return url_
            else:
                obj.user_likes.add(user)
                return url_
        return url_


def detailview(request, pk):
    post = Post.objects.get(id=pk)
    return render(request, "detail.html.j2", {'post': post})
