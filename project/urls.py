"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from blog.custome_sitemap import StaticViewSitemap, PostSitemap
from django.contrib.sitemaps import views as sitemaps_views

# info_dict = {
#     'static': StaticViewSitemap,
# }

sitemaps = {
    'static': StaticViewSitemap,
    'post': PostSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('api-blog/', include('api.urls')),
    path('', include('blog.urls')),

    path('api/v1/rest-auth/', include('rest_auth.urls')),  # new

    # path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    path('sitemap.xml/', sitemaps_views.index,
         {'sitemaps': sitemaps, 'template_name': 'sitemap_index.html'}),

    # path('sitemap.xml/', sitemap,
    #      {'sitemaps': sitemaps}),

    path('sitemap-<section>.xml/', sitemaps_views.sitemap,
         {'sitemaps': sitemaps, 'template_name': 'sitemap.html'}, name='django.contrib.sitemaps.views.sitemap'),

]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
