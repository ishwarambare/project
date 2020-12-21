from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse, reverse_lazy


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(Base):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, null=True, blank=True)
    short_description = models.CharField(blank=True, null=True, max_length=2000)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('categories', args=[self.pk], )

    def get_category_url(self):
        return reverse('post_category', args=[self.pk])


class Tag(Base):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


class Post(Base):
    name = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.CharField(max_length=500, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(max_length=2000, null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    tag = models.ManyToManyField(Tag, blank=True)
    user_likes = models.ManyToManyField(User, related_name='user_likes', blank=True)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("detail", kwargs={"pk": self.pk})

    def get_like_url(self):
        return reverse("like-toggle", kwargs={"pk": self.pk})

    def get_pdf_link(self):
        return reverse("get-pdf", kwargs={"pk": self.pk})

    class Meta:
        ordering = ['-created_at']


class ImageData(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='new_image')

    def __str__(self):
        return f'{self.name}'
