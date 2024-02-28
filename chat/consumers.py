import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.core import serializers
from django.db.models import Q
from accounts.models import Account
from . import models


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    # ----------------------------------------------------
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # ----------------------------------------------------
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_username = text_data_json['sender']
        receiver_username = text_data_json['receiver']

        # Save message to the database
        saved_message = await self.save_message(sender_username, receiver_username, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message_object': serializers.serialize('json', [saved_message,])
            }
        )

    # ----------------------------------------------------
    
    async def chat_message(self, event):
        message_object = event.get('message_object')

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message_object,
        }))

    # ----------------------------------------------------
    
    async def save_message(self, sender_username, receiver_username, message_content):
        # Retrieve users and thread based on your application logic
        # user1 = self.scope['user']
        sender = await sync_to_async(Account.objects.get)(username=sender_username)
        receiver = await sync_to_async(Account.objects.get)(username=receiver_username)
        thread = await sync_to_async(models.Thread.objects.get)((Q(user1=sender) &  Q(user2=receiver)) | (Q(user1=receiver) & Q(user2=sender)))

        # Save the message to the database
        new_message = await sync_to_async(models.Message.objects.create)(
            thread=thread,
            from_user=sender,
            to_user=receiver,
            content=message_content
        )
        
        return new_message

    # ----------------------------------------------------
    
    async def chat_room_info(self, event):
        # Send chat room information to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat.room_info',
            'room_id': event['room_id'],
            'room_name': event['room_name'],
            'room_messages': event['room_messages'],
        }))
