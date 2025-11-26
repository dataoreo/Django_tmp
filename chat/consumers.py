import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from chat.models import MessengerMessage, MessengerChannel, ChannelMember

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            await self.close()
            return

        self.channel_id = self.scope['url_route']['kwargs']['channel_id']
        self.channel_group_name = f"chat_{self.channel_id}"

        await self.channel_layer.group_add(
            self.channel_group_name,
            self.channel_name
        )

        await self.accept() # 연결 수락

    async def disconnect(self, close_code):
        if self.user.is_authenticated: # 인증된 사용자만 그룹 탈퇴 처리
            await self.channel_layer.group_discard(
                self.channel_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        sender_name = self.user.name

        await self.save_message(message, self.user)

        await self.channel_layer.group_send(
            self.channel_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender_name,
                'sent_at': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'sent_at': event['sent_at'],
        }))

    @database_sync_to_async
    def is_member(self):
        # ...
        return True

    @database_sync_to_async
    def save_message(self, content, user):
        try:
            channel = MessengerChannel.objects.get(pk=self.channel_id)

            if user.is_authenticated:
                sender_user = user
            else:
                sender_user = None

            MessengerMessage.objects.create(
                channel=channel,
                sender=sender_user,
                content=content
            )
            return True
        except MessengerChannel.DoesNotExist:
            print(f"Error: Channel with ID {self.channel_id} not found.")
            return False
        except Exception as e:
            print(f"Error saving message: {e}")
            return False