# from django.contrib.sitemaps import Sitemap  # sitemap
# from django.contrib.sitemaps.views import sitemap  # sitemap
#
# from blog.models import Post
# from django.urls import reverse
#
#
# class StaticViewSitemap(Sitemap):
#     protocol = "http"
#     priority = 0.9
#     changefreq = 'daily'
#
#     def items(self):
#         return ['home']
#
#     def location(self, item):
#         return reverse(item)
#
#
# class NewSiteMap(Sitemap):
#     protocol = "http"
#     priority = 0.9
#     changefreq = 'daily'
#
#     def items(self):
#         return Post.objects.all()
#
#     def location(self, obj):
#         return obj.get_absolute_url()
#
#
# class NewStaticViewSideMap(Sitemap):
#     protocol = "http"
#     priority = 0.9
#     changefreq = 'daily'
#
#     def items(self):
#         return ["home", "detail", 'login']
#
#     def location(self, obj):
#         return obj


from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.models import Post


class StaticViewSitemap(Sitemap):
    protocol = "http"
    priority = 0.9
    changefreq = 'daily'

    def items(self):
        return ['home',"account:login","account:register",'export']

    def location(self, item):
        return reverse(item)


class PostSitemap(Sitemap):
    protocol = "http"
    priority = 0.9
    changefreq = 'daily'
    limit = 1000

    def items(self):
        return Post.objects.all()

    # def lastmod(self, obj):
    #     return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()
