from api.views import User
from blog.models import *
from account.models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        fields = ['name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostSerializers(serializers.ModelSerializer):
    # category = CategorySerializer()
    tag = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Post
        fields = '__all__'


class SignUpSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def save(self, **kwargs):
        user = User(username=self.validated_data['username'], email=self.validated_data['email'])
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': "password must match"})
        user.set_password(password)
        user.save()
        return user
