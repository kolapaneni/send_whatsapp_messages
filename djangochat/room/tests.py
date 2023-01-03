import json
from datetime import datetime

from plyer import notification
from django.http import HttpResponse

from rest_framework.decorators import renderer_classes, api_view
from rest_framework.renderers import JSONRenderer
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

from .models import Room, Message, Conversations

dict = {
    "good morning": "Very Good morning!",
    "how are you": "I am fine. how are you",
    "hi": "Hello. Welcome to CollegeDekho.com services on whatsapp. Lovely, may i have your name?",
    "colleges": "Visit this website for best colleges https://www.collegedekho.com OR"
                "Contact us For more information +919849256029 and +917981119824",
    "hello": "Hi, Welcome to CollegeDekho.com services on whatsapp. How may i help you?",
    "default": "Sorry! I didn't get that. For more details Visit this website https://www.collegedekho.com/ OR call "
               "us for more information +919849256029, +91798119824. "

}


def get_conversation_id(phone_no1, phone_no2):
    if phone_no1 < phone_no2:
        phone_no1, phone_no2 = phone_no2, phone_no1

    return f"{phone_no1}-{phone_no2}"


@api_view(['POST'])
@renderer_classes([JSONRenderer])
def message(request):
    sender = request.POST.get('From')
    sender = int(sender.split("+")[1][2:])
    name = request.POST.get('ProfileName')
    receiver = request.POST.get('To')
    receiver = int(receiver.split("+")[1][2:])

    print(request.POST.dict)
    message = request.POST.get('Body')
    print(f'{sender} says {message}')
    notification.notify(title="message:",
                        message=f'{name} says {message}')
    incoming_msg = request.data['Body'].lower()
    resp = MessagingResponse()
    reply = dict.get(incoming_msg, dict.get("default"))
    resp.message(reply)
    print(resp)

    obj = Conversations.objects.create(room_id=get_conversation_id(sender, receiver),
                                       sender=sender, receiver=receiver, message=incoming_msg,
                                       sent_at=datetime.now())
    return HttpResponse(str(resp))


account_sid = "ACf277df7c17901f4619a31059a7f05bcf"
auth_token = "e672cd098b50c4b70ad961cf99c4f32a"
client = Client(account_sid, auth_token)


def send_whatsapp_msg(message, sender_number):
    message = client.messages.create(
        # media_url=["https://pbs.twimg.com/profile_images/1147020879961833473/5yd4usCd_400x400.png"],
        from_="whatsapp:+14155238886",
        body=message,
        to="whatsapp:+919849256029"
    )
    return message



@api_view(['POST'])
@renderer_classes([JSONRenderer])
def send_msg(request):
    message = request.POST.get['Body']
    sender_name = request.POST.get["ProfileName"]
    sender_number = request.POST.get["From"]
    print("msg:", message, "name:", sender_name, "number:", sender_number)
    message = send_whatsapp_msg(message, sender_number)
    return HttpResponse(str(message))



# @api_view(['POST'])
# @renderer_classes([JSONRenderer])
# @csrf_exempt
# def send_msg(request):
# message = client.messages.create(
#     media_url=["https://pbs.twimg.com/profile_images/1147020879961833473/5yd4usCd_400x400.png"],
#     from_="whatsapp:+14155238886",
#     body="Hello! Visit this website for better colleges. https://www.collegedekho.com",
#     to="whatsapp:+919849256029"
# )
# print(message.sid)
# return HttpResponse()
# 
# @csrf_exempt
# def wa_conversation(request):
#     conversation = client.conversations.v1.conversations.create()
#     print(request.POST.dict)
#     print(conversation.sid)
#     return HttpResponse(conversation)
# 
# 
# @csrf_exempt
# def two_way_conversation(request):
#     participant = client.conversations \
#         .v1 \
#         .conversations('CH043585dfee7d473eafc68373ac1d657c') \
#         .participants \
#         .create(messaging_binding_address='whatsapp:+919849256029',
#                 messaging_binding_proxy_address='whatsapp:+14155238886'
#     )
# 
#     print(participant.sid)
#     return HttpResponse(participant)
# 

