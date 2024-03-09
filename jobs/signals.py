from django.db.models.signals import post_save, m2m_changed, post_delete
from django.dispatch import receiver
from accounts.models import Notification
from . import models

@receiver(post_save, sender=models.ResumeFile)
def resume_file_notification_maker(sender, instance: models.ResumeFile, created, **kwargs):
    if created:
        
        Notification.objects.create(
            recipient= instance.employer,
            message=f"کاربر {instance.user} یک فایل رزومه برای شما ارسال است.",
            review_link=instance.get_absolute_url(),
        )

# --------------------------------------------------------------------

@receiver(post_save, sender=models.Resume)
def resume_notification_maker(sender, instance: models.Resume, created, **kwargs):
    if created:
        
        Notification.objects.create(
            recipient= instance.employer,
            message=f"کاربر {instance.user} یک فرم رزومه برای شما ارسال است.",
            review_link=instance.get_absolute_url(),
        )

# --------------------------------------------------------------------
