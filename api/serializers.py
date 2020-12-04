from blog.models import *
from account.models import *
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostSerializers(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Post
        fields = '__all__'
