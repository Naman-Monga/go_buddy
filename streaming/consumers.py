from channels.generic.websocket import AsyncWebsocketConsumer
# from .models import MessageModel, ThreadModel
import json
# from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

class StreamRoomConsumer(AsyncWebsocketConsumer):
    # @database_sync_to_async
    # def store_message(self, senderID, text, thread_id):
    #     thread = ThreadModel.objects.get(pk=thread_id)
    #     user = get_user_model()
    #     sender = user.objects.filter(pk=senderID)[0]
    #     if thread.receiver.id == sender:
    #         receiver = thread.user
    #     else:
    #         receiver = thread.receiver

    #     message = MessageModel()
    #     message.body = text
    #     message.thread = thread
    #     message.sender_user = sender
    #     message.receiver_user = receiver
    #     message.save()

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'stream_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type':'test_message',
        #         'message':"You're now connected",
        #     }
        # )

    # async def test_message(self, event):
    #     message = event['message']
    #     await self.send(text_data=json.dumps({
    #         'welcome':message
    #     }))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        seektime = text_data_json['seektime']
        playing = text_data_json['playing']
        user_id = text_data_json['userID']
        src_shift = text_data_json['srcShift']
        vid_src = text_data_json['vidSrc']

        # await self.store_message(user_id, message, thread_id)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'seek_time',
                'seektime':seektime,
                'playing':playing,
                'user_id':user_id,
                'src_shift':src_shift,
                'vid_src':vid_src
            }
        )


    async def seek_time(self, event):
        seektime = event['seektime']
        playing = event['playing']
        user_id = event['user_id']
        src_shift = event['src_shift']
        vid_src = event['vid_src']
        await self.send(text_data=json.dumps({
            'seektime':seektime,
            'playing':playing,
            'userID':user_id,
            'srcShift':src_shift,
            'vidSrc':vid_src
        }))
