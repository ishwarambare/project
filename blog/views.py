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
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import RedirectView, View

from blog.forms import PostForm, DateForm, ImageDataForm
from blog.models import Post, Category, ImageData
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
        form=PostForm()
        return render(request, "search_list.html.j2", {"books": status,'form':form})
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
        if form.is_valid():
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

def get_post_list(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            # name = request.POST['name']
            # category = request.POST['category']
            # description = request.POST['description']
            # post = Post(name=name, category_id=category, description=description)
            values = list(Post.objects.values())
            print("this is a get-post-list")
            return JsonResponse({'status': 'display', 'values': values})
        else:
            print("this is a get-post-list")
            return JsonResponse({'status': 0})


@csrf_exempt
def get_custome_post(request):
    date1 = request.POST.get("data1")
    date2 = request.POST.get("data2")
    print(date1)
    print(date2)
    if date1 is not None and date2 is not None:
        try:
            # post = list(Post.objects.filter(Q(created_at__gte=date1) & Q(created_at__lte=date2)).values())
            post = Post.objects.filter(Q(created_at__gte=date1) & Q(created_at__lte=date2))
            print(post)

            data = get_template('new_custome_post.html.j2').render({"post": post})
            return JsonResponse({"post": data},safe=False)


        except Exception as e:
            post = Post.objects.all()

            data = get_template('new_custome_post.html.j2').render({"post": post})
            return JsonResponse({"post": data}, safe=False)
            # return JsonResponse({'error': str(e)})

    form = DateForm()
    post = Post.objects.all()
    return render(request, 'custome_post.html.j2', {'post': post, 'form': form})


import base64
from django.core.files.base import ContentFile


def base64_file(data, name=None):
    pass
    # _format, _img_str = data.split(';base64,')
    # _name, ext = _format.split('/')
    # if not name:
    #     name = _name.split(":")[-1]
    # return ContentFile(base64.b64decode(_img_str), name='{}.{}'.format(name, ext))


def base_64_image(request):
    if request.method == "POST":
        form = ImageDataForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            user.save()
            return HttpResponse("Image Save", data)
        else:
            return HttpResponse("please check creadentioals")
    else:
        form = ImageDataForm()
        return render(request, 'base_64_image.html.j2', {'form': form})
