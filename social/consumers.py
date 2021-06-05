from channels.generic.websocket import AsyncWebsocketConsumer
from .models import MessageModel, ThreadModel
import json
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model


class ChatRoomConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def store_message(self, senderID, text, thread_id):
        thread = ThreadModel.objects.get(pk=thread_id)
        user = get_user_model()
        sender = user.objects.filter(pk=senderID)[0]
        if thread.receiver.id == sender:
            receiver = thread.user
        else:
            receiver = thread.receiver

        message = MessageModel()
        message.body = text
        message.thread = thread
        message.sender_user = sender
        message.receiver_user = receiver
        message.save()

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'test_message',
                'message':"You're now connected",
            }
        )

    async def test_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'welcome':message
        }))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['user']
        thread_id = text_data_json['thread']
        user_id = text_data_json['userID']
        await self.store_message(user_id, message, thread_id)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chatroom_message',
                'message':message,
                'userID':user_id
            }
        )


    async def chatroom_message(self, event):
        message = event['message']
        user_id = event['userID']
        await self.send(text_data=json.dumps({
            'message':message,
            'sender':user_id
        }))
