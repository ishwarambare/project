from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import Environment
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_form, as_crispy_field


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        "as_crispy": as_crispy_form,
        'url': reverse,
    })

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
