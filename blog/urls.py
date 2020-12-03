from django.urls import path
from . import views
app_name = 'blog'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name="login"),
    path('home/', views.main, name="home"),
    path('logout/', views.logout_view, name="logout"),
    path('', views.home, name="home"),
    path('form/', views.post_view_form, name="form"),
    path('search/', views.search, name="search"),


]

