# import markdown
# from crispy_forms.templatetags.crispy_forms_filters import as_crispy_form, as_crispy_field
from django.contrib.staticfiles.storage import staticfiles_storage
from django.db.models import Count
from django.urls import reverse
from django.utils.safestring import mark_safe
# from jinja2 import Environment

from blog.models import Post


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        "crispy": as_crispy_form,
        "as_crispy": as_crispy_field,
        "total_posts": total_posts,
        "show_latest_posts": show_latest_posts,
        "markdown_format": markdown_format,
        "get_most_commented_posts": get_most_commented_posts,
        'url': reverse,
    })

    env.filters['total_posts'] = total_posts
    env.filters['show_latest_posts'] = show_latest_posts
    env.filters['markdown'] = markdown_format

    return env


'''

def total_posts():
    return Post.published.count()


def show_latest_posts(count=5):
# def show_latest_posts():
    # latest_posts = Post.published.order_by('-publish')[:count]
    latest_posts = Post.objects.all().order_by('-publish')[:count]
    # latest_posts = Post.published.order_by('-publish')[:3]
    # return {'latest_posts': latest_posts}
    return latest_posts


def get_most_commented_posts(count=5):
    return Post.published.annotate(
               total_comments=Count('comments')
           ).order_by('-total_comments')[:count]


def markdown_format(text):
    return mark_safe(markdown.markdown(text))


'''