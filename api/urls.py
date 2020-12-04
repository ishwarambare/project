from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('', views.home),
    path('post/', views.PostView.as_view()),

]
