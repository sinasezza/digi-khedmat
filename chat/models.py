from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
import uuid


class Thread(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
        return reverse('chat:chat-room', kwargs={'room_id': self.id})

# =====================================================================

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # -------------------------------------------------
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')
    # -------------------------------------------------
    from_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='sent_messages')
    # -------------------------------------------------
    to_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='received_messages')
    # -------------------------------------------------
    content = models.CharField(max_length=255, blank=True, null=True)
    # -------------------------------------------------
    created_at = models.DateTimeField(auto_now_add=True)
    # -------------------------------------------------

    def __str__(self):
        return f"Message from {self.from_user} to {self.to_user}"

    
    
