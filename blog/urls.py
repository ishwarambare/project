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

    # path('signup-new/', views.SignUpView.as_view(), name='signup-new'),
    #
    # path('ajax/validate_username/', views.validate_username, name='validate_username'),

]
