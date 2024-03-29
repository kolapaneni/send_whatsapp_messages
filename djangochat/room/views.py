import json
import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from .utils import send_notification
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from datetime import datetime
from twilio.rest import Client
from rest_framework.decorators import api_view, renderer_classes
from .tests import get_conversation_id
from django.conf import settings
from .models import Room, Message, Conversations


# x = ["+917981119824", "+917702025720", "+919160032524"]
# for i in x:
#     pywhatkit.sendwhatmsg_instantly(i, "Good Morning!")


@login_required
def rooms(request):
    rooms = Room.objects.all()

    return render(request, 'room/rooms.html', {'rooms': rooms})


@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)[0:100]

    return render(request, 'room/room.html', {'room': room, 'messages': messages})


account_sid = "ACf277df7c17901f4619a31059a7f05bcf"
auth_token = "e672cd098b50c4b70ad961cf99c4f32a"
client = Client(account_sid, auth_token)


@renderer_classes([JSONRenderer])
def wts_message(request):
    message = client.messages.create(
        media_url=["https://pbs.twimg.com/profile_images/1147020879961833473/5yd4usCd_400x400.png"],
        from_="whatsapp:+14155238886",
        body="Hello! Visit this website for better colleges. https://www.collegedekho.com",
        to="whatsapp:+919849256029"
    )
    print(message.sid)
    return HttpResponse(str(message))


###### WHATSAPP BUSINESS API PROVIDED BY FB META DEVELOPER ############

class Whatsappwebhook(APIView):
    def get(self, request):
        VERIFY_TOKEN = settings.WEBHOOK_VERIFY_TOKEN
        mode = request.GET['hub.mode']
        token = request.GET['hub.verify_token']
        challenge = request.GET['hub.challenge']

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return HttpResponse(challenge)
        else:
            return HttpResponse('error')

    def post(self, request):
        data = json.loads(request.body)
        print(data)

        if 'object' in data and 'entry' in data:
            try:
                for entry in data['entry']:
                    phoneNumber = entry['changes'][0]['value']['metadata']['display_phone_number']
                    phoneId = entry['changes'][0]['value']['metadata']['phone_number_id']
                    profileName = entry['changes'][0]['value']['contacts'][0]['profile']['name']
                    whatsAppId = entry['changes'][0]['value']['contacts'][0]['wa_id']
                    fromId = entry['changes'][0]['value']['messages'][0]['from']
                    messageId = entry['changes'][0]['value']['messages'][0]['id']
                    timestamp = entry['changes'][0]['value']['messages'][0]['timestamp']
                    text = entry['changes'][0]['value']['messages'][0]['text']['body'].lower()
                    
                    dict = {
                        "hi": f"Hello, {profileName}"
                    }
                    incoming_msgs = text

                    obj = Conversations.objects.create(room_id=get_conversation_id(fromId, phoneNumber),
                                                       sender=fromId, receiver=phoneNumber, message=incoming_msgs,
                                                       sent_at=datetime.now())
                    reply = dict.get(incoming_msgs)

                    sendwhatsappmessages(fromId, reply)
            except:
                pass
            return HttpResponse('success', status=200)


def sendwhatsappmessages(phoneNumber, message):
    headers = {"Authorization": settings.WHATSAPP_TOKEN}
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": phoneNumber,
        "type": "text",
        "text": {"body": message}
    }
    response = requests.post(settings.WHATSAPP_URL, headers=headers, json=payload)
    ans = response.json()
    return ans


######## INFOBIP WHATSAPP API #######################
class InfobipAPIView(APIView):
    def post(self, request):
        data = json.loads(request.body)
        print(data)
        if 'results' in data:
            try:
                for i in data['results']:
                    from_ = i['from']
                    print(from_)
                    to = i['to']
                    msg = i['message']['text']
                    profile_name = i['contact']['name']
                    send_notification(message=msg)
                    dict = {
                        "good morning": "Very Good morning!",
                        "how are you": "I am fine. how are you",
                        "hi": f"Hello {profile_name}, Welcome to CollegeDekho.com services on whatsapp. Lovely, may i "
                              f"have your name?",
                        "colleges": f"Hi {profile_name}, Visit this website for best colleges "
                                    f"https://www.collegedekho.com OR"
                                    "Contact us For more information +919849256029 and +917981119824",
                        "hello": f"Hi {profile_name}, Welcome to CollegeDekho.com services on whatsapp. How may i help "
                                 f"you?",
                        "default": f"Sorry!{profile_name}, I didn't get that. For more details Visit this website "
                                   f"https://www.collegedekho.com/ OR call"
                                   "us for more information +919849256029, +91798119824. "

                    }
                    incoming_msgs = msg.lower()
                    obj = Conversations.objects.create(room_id=get_conversation_id(from_, to),
                                                       sender=from_, receiver=to, message=msg,
                                                       sent_at=datetime.now())
                    reply = dict.get(incoming_msgs, dict.get('default'))

                    # message = f"Hello {profile_name}, Welcome to CollegeDekho services. How may i help you?"
                    sendinfobipmessage(from_, reply, to)
            except:
                pass
                
            return HttpResponse('success', status=200)


def sendinfobipmessage(phonenumber, message, sender):
    # sender = "447860099299"
    # RECIPIENT = "919849256029"

    payload = {
        "from": sender,
        "to": phonenumber,
        "content": {
            "text": message,
        }
    }
    headers = {
        'Authorization': settings.INFOBIP_API_KEY,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.post(settings.INFOBIP_URL + "/whatsapp/1/message/text", json=payload, headers=headers)
    ans = response.json()
    return ans