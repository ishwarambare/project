from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('', views.home),
    path('post/', views.PostView.as_view()),
    path('post-category/', views.CategoryView.as_view()),
    path('login/', views.LoginView.as_view({'post': 'login'})),
    # path('signup/', views.SignUpView.as_view({'post': 'signup'})),
    path('signup/', views.sign_up_view.as_view()),
    path('search/', views.SearchPost.as_view()),
    path('post-detail/<int:pk>', views.post_detail),

    path('post-uplode', views.PostUplodeView.as_view(), name='post-uplode'),

    path('post-uplode-new/', views.PostApiUplode.as_view(), name='post-uplode-new'),


    path('image-data-view/', views.ImageDataView.as_view(), name='image-data-view'),


]
