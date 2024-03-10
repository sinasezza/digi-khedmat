from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
import uuid


class Thread(models.Model):
    name = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # -------------------------------------------------
    user1 = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='my_threads')
    # -------------------------------------------------
    user2 = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='others_threads')
    # -------------------------------------------------

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user1', 'user2'], name='unique_chat_thread'),
        ]

    # -------------------------------------------------

    def __str__(self):
        return f"Chat between {self.user1} and {self.user2}"
    
    # -------------------------------------------------
    
    def get_room_url(self):
        return reverse('chat:chat-room', kwargs={'room_name': self.name})

# =====================================================================

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # -------------------------------------------------
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')
    # -------------------------------------------------
    from_user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, related_name='sent_messages')
    # -------------------------------------------------
    to_user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, related_name='received_messages')
    # -------------------------------------------------
    content = models.CharField(max_length=255, blank=True, null=True)
    # -------------------------------------------------
    created_at = models.DateTimeField(auto_now_add=True)
    # -------------------------------------------------

    def __str__(self):
        return f"Message from {self.from_user} to {self.to_user}"

    
# =====================================================================

class Report(models.Model):
    thread = models.ForeignKey(to=Thread, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports', verbose_name="کفت و گو")
    # -------------------------------------------------
    reporter = models.ForeignKey(to=get_user_model(), on_delete=models.SET_NULL, null=True, related_name='reports', verbose_name="گزارش دهنده")
    # -------------------------------------------------
    message = models.TextField(max_length=400, verbose_name="پیام گزارش")
    # -------------------------------------------------
    date_reported = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ گزارش")
    
