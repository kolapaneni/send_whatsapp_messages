import json
import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from twilio.rest import Client
from rest_framework.decorators import api_view, renderer_classes

from djangochat import settings
from .models import Room, Message


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

@csrf_exempt
def whatsappwebhook(request):
    if request.method == 'GET':
        VERIFY_TOKEN = '1d731114-f447-4e87-b43e-8e858414ef95'
        mode = request.GET['hub.mode']
        token = request.GET['hub.verify_token']
        challenge = request.GET['hub.challenge']

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return HttpResponse(challenge)
        else:
            return HttpResponse('error')

    if request.method == 'POST':
        data =json.loads(request.body)
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
                    text = entry['changes'][0]['value']['messages'][0]['text']['body']
                    print(text)

                    # phoneNumber = "918149689641"
                    message = "Hi, {}. Welcome to CollegeDekho.com services on whatsapp. How may i help you?".format(profileName)
                    sendwhatsappmessages(fromId, message)
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
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def infobip(request):
    data = request.POST.dict
    print(data)