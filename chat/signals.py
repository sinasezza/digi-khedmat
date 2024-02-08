from django.db.models.signals import post_save, m2m_changed, post_delete
from notifications.models import Notification
from notifications.signals import notify
from django.dispatch import receiver
from . import models

@receiver(post_save, sender=models.Message)
def my_handler(sender, instance, created, **kwargs):
    if created:
        notify.send(sender=instance.from_user, recipient=instance.to_user, verb='شما یک پیام دریافت کردید')
    # notify.send(instance.author, recipient=instance.recipient, action=notify.Action)
    
