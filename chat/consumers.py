# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        await self.channel_layer.group_add(
            "chat_group",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "chat_group",
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        x_position = text_data_json.get('x_position', 100)  # Default position if not provided
        y_position = text_data_json.get('y_position', 100)  # Default position if not provided

        await self.channel_layer.group_send(
            "chat_group",
            {
                'type': 'chat_message',
                'message': message,
                'user_id': self.user.id,
                'nickname': self.user.nickname,
                'x_position': x_position,
                'y_position': y_position,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        user_id = event['user_id']
        nickname = event['nickname']
        x_position = event['x_position']
        y_position = event['y_position']

        await self.send(text_data=json.dumps({
            'message': message,
            'user_id': user_id,
            'nickname': nickname,
            'x_position': x_position,
            'y_position': y_position,
        }))
