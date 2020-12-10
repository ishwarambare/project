from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from rest_framework import generics, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Post, Category
from .serializers import PostSerializers, CategorySerializer, SignUpSerializer


def home(request):
    return HttpResponse('hello')


class PostView(APIView):
    def get(self, request):
        try:
            post = Post.objects.all()
            data = PostSerializers(post, many=True).data
            return Response(data={'status': True, "message": "success", "data": data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'status': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CategoryView(APIView):
    def get(self, request):
        try:
            objects_all = Category.objects.all()
            data = CategorySerializer(objects_all, many=True).data
            return Response(data={'status': True, "message": "success", "data": data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'status': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(viewsets.ViewSet):
    authentication_classes = ()
    permission_classes = ()

    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            username = User.objects.get(username=username)
        except Exception:
            return Response(data={'status': False, 'message': 'Invalid Credential'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is None:
            return Response(data={'status': False, 'message': 'Invalid Credential'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            login(request, user)
            return Response(data={'status': True, 'message': 'Authentication successfull'},
                            status=status.HTTP_200_OK)


class SignUpView(viewsets.ViewSet):
    authentication_classes = ()
    permission_classes = ()

    def signup(self, request):
        data = request.data
        try:
            username = data.get('username')
            if not User.objects.filter(username=request.user).exists():
                return Response(data={'status': False, 'message': 'User Already exist', 'is_dms_match': True},
                                status=status.HTTP_400_BAD_REQUEST)

            email = data.get('email')
            password = data.get('password')
            data = {
                'username': username,
                'email': email,
            }
            user = User.objects.filter(username=request.user).update(**data)
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            return Response(data={'status': True, 'message': 'User registered'},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'status': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class sign_up_view(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        if request.method == 'POST':
            serializer = SignUpSerializer(data=request.data)
            data = {}
            if serializer.is_valid():
                user = serializer.save()
                data['response'] = 'successful register user name'
                data['email'] = user.email
                data['username'] = user.username
            else:
                data = serializer.errors
            return Response(data)


class SearchPost(generics.ListAPIView):
    permission_classes = ()
    serializer_class = PostSerializers

    def get_queryset(self):
        data = self.request.data
        search_data = data.get('search')
        post = Post.objects.filter(Q(category__name__icontains=search_data) |
                                   Q(description__icontains=search_data))
        return post


@api_view(['GET', ])
def post_detail(request, pk):
    try:
        snippet = Post.objects.get(pk=pk)
    except Exception as e:
        return Response(data={'status': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = PostSerializers(snippet)
        return Response(
            data={'status': True, "message": "success", "data": serializer.data, },
            status=status.HTTP_200_OK)


class PostUplodeView(generics.CreateAPIView):
    queryset = Post.objects.all()
    authentication_classes = ()
    permission_classes = ()
    serializer_class = PostSerializers


class PostApiUplode(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        try:
            name = request.data['name']
            print(name)
            category_id = request.data['category_id']
            print(category_id)
            description = request.data['description']
            print(description)
            user_id = request.data['user_id']
            # if User.objects.get(id=user_id) and Category.objects.get(name=category_id):
            post = Post.objects.create(
                user_id=user_id,
                name=name,
                category_id=category_id,
                description=description
            )
            post_save = post.save()
            last = Post.objects.all().last()
            data = PostSerializers(last).data
            return Response({"result": data})
        except Exception as e:
            return Response(data={'status': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
