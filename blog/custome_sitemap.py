from django.contrib.sitemaps import Sitemap  # sitemap
from django.contrib.sitemaps.views import sitemap  # sitemap

from blog.models import Post
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    protocol = "http"
    priority = 0.9
    changefreq = 'daily'

    def items(self):
        return ['blog:home']

    def location(self, item):
        return reverse(item)


class NewSiteMap(Sitemap):
    protocol = "http"
    priority = 0.9
    changefreq = 'daily'

    def items(self):
        return Post.objects.all()

    def location(self, obj):
        # return obj.updated_at
        return obj.get_absolute_url()


class NewStaticViewSideMap(Sitemap):
    protocol = "http"
    priority = 0.9
    changefreq = 'daily'

    def items(self):
        return ["blog:home", "blog:detail", "blog:post_category", "blog:categories"]

    def location(self, obj):
        return obj
