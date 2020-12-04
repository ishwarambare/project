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
    slug = models.SlugField(max_length=200, unique=True)
    short_description = models.CharField(blank=True, null=True, max_length=2000)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('blog:categories', args=[self.pk], )

    def get_category_url(self):
        return reverse('blog:post_category', args=[self.pk])


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
    post = models.ManyToManyField(Tag, null=True, blank=True)
    likes = models.PositiveIntegerField(default=0)
    user_likes = models.ManyToManyField(User, related_name='user_likes', null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"pk": self.pk})

    def get_like_url(self):
        return reverse("blog:like-toggle", kwargs={"pk": self.pk})


class Comment(Base):
    comment = models.CharField(max_length=500)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="posts")
    value = models.IntegerField()
    alreadyLiked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} liked {self.post}"

    class Meta:
        unique_together = ("user", "post", "value")
