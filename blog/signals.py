from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Post  # likes - total_likes
                          # user_likes - users_like


@receiver(m2m_changed, sender=Post.user_likes.through)
def users_like_changed(sender, instance, **kwargs):
    instance.likes = instance.user_likes.count()
    instance.save()

