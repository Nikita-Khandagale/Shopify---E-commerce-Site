from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from userapp.models import User, UserProfile


# When a new user is created → create profile automatically
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


# When a user is saved → save linked profile
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)


# When profile is deleted → delete linked user
@receiver(post_delete, sender=UserProfile)
def delete_user_when_profile_deleted(sender, instance, **kwargs):
    user = instance.user
    if user:
        user.delete()
