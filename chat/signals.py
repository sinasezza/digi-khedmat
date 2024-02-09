from django.db.models.signals import post_save, m2m_changed, post_delete
from django.dispatch import receiver
from accounts.models import Notification
from . import models

@receiver(post_save, sender=models.Thread)
def my_handler(sender, instance: models.Thread, created, **kwargs):
    if created:
        
        Notification.objects.create(
            recipient= instance.user2,
            message=f"کاربر {instance.user1} یک صفحه چت با شما ایجاد کرده است.",
            review_link=instance.get_room_url(),
        )
    
