from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    # path('login/', views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html.j2'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html.j2'), name='logout'),
]
