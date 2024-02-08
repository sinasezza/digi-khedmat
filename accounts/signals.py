from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save, m2m_changed, post_delete
from notifications.signals import notify
from django.dispatch import receiver
from notifications.models import Notification
from django.contrib.auth import get_user_model


@receiver(post_save, sender=Notification)
def notification_created(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'public_room',
            {
                "type": "user_notification",
                "message": instance.verb
            }
        )
        print("sldfj;lasdjf;l \n\n lsdflsdj\n\n")