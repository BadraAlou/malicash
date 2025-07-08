from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         # Récupère le numéro de téléphone temporairement stocké dans l’instance
#         phone = getattr(instance, '_phone', None)
#         Profile.objects.create(user=instance, phone=phone)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:  # Vérifie si l'utilisateur est nouvellement créé
        # Vérifie si un profil existe déjà pour cet utilisateur
        if not Profile.objects.filter(user=instance).exists():
            Profile.objects.create(user=instance, phone="")

# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     if hasattr(instance, 'profile'):
#         instance.profile.save()

# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()

# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)