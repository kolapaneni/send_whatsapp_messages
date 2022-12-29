from django.urls import path
from . import consumer, utils

websocket_urlpatterns = [
    path("<int:sender>/<int:receiver>", consumer.ChatConsumer.as_asgi()),
    path('ws/<str:room_name>/', utils.ChatConsumer.as_asgi()),
]
