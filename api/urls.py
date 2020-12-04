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

]
