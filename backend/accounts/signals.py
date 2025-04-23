from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from .utils import send_otp_mail



@receiver(post_save, sender=CustomUser)
def send_otp_mail(sender, instance, created, **kwargs):
    if created:
        send_otp_mail(instance)
    return