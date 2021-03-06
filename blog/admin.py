from django.contrib import admin
from blog.models import Post, Category, Tag, ImageData, User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _


class CustomeUser(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password','email')}),
        (_('Personal info'), {'fields': (
            'birth_date',
        )}),)

    list_display = ['username', 'email','birth_date']


class PostAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    prepopulated_fields = {"slug": ("name",)}


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag)
admin.site.register(ImageData)
admin.site.register(User, CustomeUser)