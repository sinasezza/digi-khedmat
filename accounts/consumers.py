import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from notifications.models import Notification


class NotificationsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        user = self.scope['user']
        if user.is_authenticated:
            await self.channel_layer.group_add(
                f"user-{user.id}", self.channel_name
            )

    async def disconnect(self, close_code):
        user = self.scope['user']
        if user.is_authenticated:
            await self.channel_layer.group_discard(
                f"user-{user.id}", self.channel_name
            )

    async def user_notification(self, event):
        notification = event['notification']
        data = {
            'count': Notification.objects.filter(
                recipient=self.scope['user'], unread=True
            ).count()
        }
        await self.send(text_data=json.dumps(data))
        


