import json
from channels.generic.websocket import AsyncWebsocketConsumer
from . import models

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"
        print(f"\n\n\n Connecting to room: {self.room_name} \n\n\n")

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Save message to the database
        await self.save_message(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': message,
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
        }))

    async def save_message(self, message_content):
        # Retrieve users and thread based on your application logic
        user1 = self.scope['user']
        user2 = None  # Set the second user based on your application logic
        thread = None  # Set the thread based on your application logic

        # Save the message to the database
        await models.Message.objects.create(
            thread=thread,
            from_user=user1,
            to_user=user2,
            content=message_content
        )

    async def chat_room_info(self, event):
        # Send chat room information to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat.room_info',
            'room_id': event['room_id'],
            'room_name': event['room_name'],
            'room_messages': event['room_messages'],
        }))
