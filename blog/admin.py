from django.contrib import admin
from blog.models import Post, Category, Tag


class PostAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    prepopulated_fields = {"slug": ("name",)}


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag)
