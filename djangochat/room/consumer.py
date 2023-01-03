import json
from datetime import datetime
import asyncio
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Conversations
from plyer import notification
from .serializers import ConversationsSerializer
from .tests import send_msg, send_whatsapp_msg
from .views import sendinfobipmessage

class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.receiver = None
        self.sender = None
        self.room_id = None

    def serialize_conversation(self, data, many=False):
        return ConversationsSerializer(data, many=many).data

    @sync_to_async
    def serialize(self, data, many=False):
        return self.serialize_conversation(data, many=many)

    async def send_message(self, data):
        # print("data:",data)
        await self.send(text_data=json.dumps(data))

    @sync_to_async
    def get_new_messages(self, sent_after):
        conversations = Conversations.objects.filter(room_id=self.room_id,
                                                     sent_at__gte=sent_after)
        # print(conversations.query, conversations.count())
        if conversations.exists():
            print("new conversation")
            data = self.serialize_conversation(conversations, many=True)
            return data

    async def fetch_new_messages(self):
        sent_after = datetime.now()
        while True:
            print("running")
            data = await self.get_new_messages(sent_after=sent_after)
            sent_after = datetime.now()
            print(data)
            if data:
                await self.send_message(data)

            await asyncio.sleep(2)

    async def connect(self):
        self.sender = self.scope['url_route']['kwargs']['sender']
        self.receiver = self.scope['url_route']['kwargs']['receiver']
        self.room_id = self.get_conversation_id(self.sender, self.receiver)

        # await self.channel_layer.group_add(
        #     self.room_id,
        #     self.channel_name
        # )

        await self.accept()
        conversations = Conversations.objects.filter(room_id=self.room_id)
        data = await self.serialize(conversations, many=True)

        await self.send_message(data=data)
        asyncio.ensure_future(self.fetch_new_messages())

    @sync_to_async
    def send_whats_app_message(self, message, phonenumber):
        sendinfobipmessage(message=message, phonenumber=phonenumber)

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']

        await self.send_whats_app_message(message, self.receiver)
        notification.notify(title="message:", message=f'{self.sender} says {message}',app_name="CollegeDekho",app_icon="https://pbs.twimg.com/profile_images/1147020879961833473/5yd4usCd_400x400.png")
        await self.save_message(sender=self.sender,
                                receiver=self.receiver,
                                message=message)

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        # username = event['username']
        # print(message, username)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            # 'username': username
        }))

    def get_conversation_id(self, phone_no1, phone_no2):
        if phone_no1 < phone_no2:
            phone_no1, phone_no2 = phone_no2, phone_no1

        return f"{phone_no1}-{phone_no2}"

    @sync_to_async
    def save_message(self, sender, receiver, message):
        obj = Conversations.objects.create(room_id=self.room_id,
                                           sender=sender, receiver=receiver, message=message,
                                           sent_at=datetime.now())
        return obj

# import json
# 
# from asgiref.sync import sync_to_async
# from channels.generic.websocket import AsyncWebsocketConsumer
# 
# from . models import Message, Room
# from django.contrib.auth.models import User
# 
# 
# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = "chat_%s" % self.room_name
# 
#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name, self.channel_name
#         )
# 
#         await self.accept()
# 
#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name, self.channel_name
#         )
# 
#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data["message"]
#         username = data["username"]
#         room = data["room"]
#         
#         # await self.connect()
# 
#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name, {
#                 "type": "chat_message",
#                 "message": message,
#                 "username": username,
#                 "room": room,
# 
#             }
#         )
# 
#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event["message"]
#         username = event["username"]
#         room = event["room"]
# 
#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             "message": message,
#             "username": username,
#             "room": room,
#         }))
# 
# @sync_to_async
# def save_messages(self, username, room, messages):
#     user = User.objects.get(username=username)
#     room = Room.objects.get(slug=room)
#     
#     Message.objects.create(user=user, room=room, content=messages)
