from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import get_template
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import RedirectView

from blog.forms import PostForm
from blog.models import Post, Category
from .forms import LoginForm


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
            return redirect('blog:home')
    else:
        return render(request, 'list.html.j2')


@login_required
def home(request, pk=None):
    post = Post.objects.all()
    categories = Category.objects.all()
    category = None
    if pk:
        category = get_object_or_404(Category, pk=pk)
        post = Post.objects.filter(category=category)

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
                                                'category': category,
                                                'categories': categories,
                                                })
    else:
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

        return render(request, 'list.html.j2', {'post': post,
                                                'page': page,
                                                'form': form,

                                                'category': category,
                                                'categories': categories,
                                                })


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


from django.http import HttpResponse
from django.views.generic import View
from .utils import render_to_pdf


class GeneratePDF(View):
    def get(self, request, pk, *args, **kwargs):
        template = get_template('post.html.j2')
        post = Post.objects.get(id=pk)
        context = {
            'post': post
        }
        html = template.render(context)
        pdf = render_to_pdf('post.html.j2', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "post_%s.pdf" % "12341231"
            content = "inline; filename='%s'" % filename
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % filename
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
