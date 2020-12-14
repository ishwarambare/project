import csv
import io

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import get_template
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import RedirectView, View

from blog.forms import PostForm
from blog.models import Post, Category
from .forms import LoginForm
from .utils import render_to_pdf


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
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
                return redirect('home')
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
    return redirect("login")


def post_view_form(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)  # use
            profile.user = request.user
            profile.save()
            return redirect('home')
        else:
            return redirect('home')
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
        return HttpResponseRedirect(reverse('home'))


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


import xlsxwriter
from django.shortcuts import render


def get_xml_file(request, *args, **kwargs):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    format2 = workbook.add_format({'num_format': 'dd/mm/yy'})
    worksheet.write(1, 0, 'post title')
    worksheet.write(1, 1, 'description')
    worksheet.write(1, 2, 'category ')
    worksheet.write(1, 3, 'date')
    worksheet.write(1, 4, 'username')
    data = Post.objects.all()
    num = 2
    for new in data:
        worksheet.write(num, 0, new.name)
        worksheet.write(num, 1, new.description)
        worksheet.write(num, 2, new.category.name)
        date_here = new.created_at.replace(tzinfo=None)
        worksheet.write(num, 3, date_here, format2)
        worksheet.write(num, 4, new.user.username)
        num += 1
    workbook.close()
    output.seek(0)
    filename = 'django_simple.xlsx'
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    output.close()
    return response


def get_csv_file(request, *args, **kwargs):
    csv_data = io.StringIO()
    csv_writer = csv.writer(csv_data)
    post_data = ['post title', 'description', 'category ', 'date', 'username']
    csv_writer.writerow(post_data)
    data = Post.objects.all()
    for row in data:
        csv_writer.writerow([row.name, row.description, row.category.name, row.updated_at, row.user.username])
    csv_data.seek(0)
    filename = 'post_simple.csv'
    response = HttpResponse(csv_data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    csv_data.close()
    return response


def fileexport(request):
    objects_all = Post.objects.all()
    return render(request, 'export.html.j2', {"post": objects_all})


def add_blog(request):
    form = PostForm()
    return render(request, 'ajax_from.html.j2', {'form': form})


from django.core import serializers


def postUplode(request):
    if request.is_ajax and request.method == "POST":
        form = PostForm(request.POST)
        print(form)
        if form.is_valid():
            print(form)
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            ser_instance = serializers.serialize('json', [instance, ])
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            return JsonResponse({"error": form.errors}, status=400)
    return JsonResponse({"error": ""}, status=400)


def checkPostName(request):
    if request.is_ajax and request.method == "GET":
        post_name = request.GET.get("name", None)
        if Post.objects.filter(name__icontains=post_name).exists():
            return JsonResponse({"valid": False}, status=200)
        else:
            return JsonResponse({"valid": True}, status=200)
    return JsonResponse({}, status=400)



# def postUplode(request):
#     if request.method == "POST":
#         form = PostForm(request.POST)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.user = request.user
#             instance.save()
#             ser_instance = serializers.serialize('json', [instance, ])
#             return JsonResponse({"instance": ser_instance}, status=200)
#         else:
#             return JsonResponse({"error": form.errors}, status=400)
#     return JsonResponse({"error": ""}, status=400)

