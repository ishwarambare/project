from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('', views.home, name="home"),

    path('<pk>', views.home, name="post_category"),

    path('form/', views.post_view_form, name="form"),
    path('search/', views.search, name="search"),
    path('categories/<int:pk>', views.categories, name="categories"),
    # path('like/<int:post_id>', views.like, name="like"),
    path('like/', views.image_like, name="like"),

    path('detail/<pk>', views.detailview, name="detail"),

    path('detail/<pk>/like/', views.PostLikeToggle.as_view(), name='like-toggle'),

    path('get-pdf/<pk>/', views.GeneratePDF.as_view(), name='get-pdf'),

    path('export/', views.fileexport, name='export'),

    path('export-csv/', views.get_csv_file, name='get-csv'),
    path('export-xml/', views.get_xml_file, name='get-xml'),

    path('add-blog/', views.add_blog, name="add-blog"),


    path('post/ajax/post', views.postUplode, name="post_uplode"),
    path('get/ajax/validate/postname', views.checkPostName, name="validate_postname"),



    path('get-post-list/', views.get_post_list, name="get-post-list"),


    path('get-custome-post/', views.get_custome_post, name="get_custome_post"),


    path('base-64-image/', views.base_64_image, name="base_64_image"),



    path('my-new-cron-job1/', views.my_new_cron_job1, name="my_new_cron_job1"),

    # path('signup-new/', views.SignUpView.as_view(), name='signup-new'),
    # path('ajax/validate_username/', views.validate_username, name='validate_username'),
]
