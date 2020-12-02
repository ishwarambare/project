from django.contrib.auth.models import User
from django.db import models


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(Base):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)
    short_description = models.CharField(blank=True, null=True, max_length=2000)


class Tag(Base):
    name = models.CharField(max_length=100)


class Post(Base):
    name = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.CharField(max_length=500, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(max_length=2000, null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    post = models.ManyToManyField(Tag)
    likes = models.PositiveIntegerField(default=0)
    user_likes = models.ManyToManyField(User, related_name='user_likes')


class Comment(Base):
    comment = models.CharField(max_length=500)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
