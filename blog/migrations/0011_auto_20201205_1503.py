# Generated by Django 3.1.4 on 2020-12-05 09:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0010_auto_20201205_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='user_likes',
            field=models.ManyToManyField(blank=True, related_name='user_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
