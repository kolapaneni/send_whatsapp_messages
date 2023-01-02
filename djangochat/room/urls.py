from django.urls import path
from . import views, tests

urlpatterns = [
    path('', views.rooms, name='rooms'),
    path('<slug:slug>/', views.room, name='room'),
    path('message', tests.message),
    path('send', tests.send_msg),
    path('test', tests.send_whatsapp_msg),
    path('whatsapp', views.wts_message),
    path('3a1b90ad-d843-478d-b4f9-35168fbaf4b9', views.whatsappwebhook, name="webhook"),
    path('infobip', views.infobip, name='infobip'),
]