import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'global_chat'
        self.room_group_name = 'chat_%s' % self.room_name

        # انضمام إلى المجموعة
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # مغادرة المجموعة
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # استقبال رسالة من WebSocket

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        
        saved_message = await self.save_message(username, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'id': saved_message.id,  # نرسل id مع الرسالة
            }
        )

    @database_sync_to_async
    def save_message(self, username, content):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.get(username=username)
        return Message.objects.create(user=user, content=content)


    # استقبال رسالة من المجموعة
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
            'id': event['id'],  # نمرر الـ id لجافاسكربت
        }))

