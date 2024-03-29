from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import UserProfile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = UserProfile.objects.create(
            user=user,
            email=user.email,
            name=user.first_name,
        )


@receiver(post_delete, sender=UserProfile)
def delete_user_profile(sender, instance, **kwargs):
    user = instance.user
    user.delete()


@receiver(post_save, sender=UserProfile)
def update_user(sender, instance, created, **kwargs):
    profile = instance
    user = instance.user

    if not created:
        user.first_name = profile.name
        user.email = profile.email

        user.save()
