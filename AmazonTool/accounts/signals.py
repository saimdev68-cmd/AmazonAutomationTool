from django.db.models.signals import post_save
from .models import User
from seller.models import Seller
from django.dispatch import receiver

@receiver(post_save,sender=User)
def create_seller(instance,created,**kwargs):
    if created:
        Seller.objects.create(
            user=instance,
            business_name=instance.full_name
        )