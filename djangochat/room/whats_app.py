# import requests
# 
# from djangochat import settings
# 
# 
# def sendwhatsappmessages(phonenumber, message):
#     headers = {"Authorization": settings.WHATSAPP_TOKEN}
#     payload = {
#         "messaging_product": "whatsapp",
#         "recipient_type": "individual",
#         "to": phonenumber,
#         "type": "text",
#         "text": {"body": message}
#     }
#     response = requests.post(settings.WHATSAPP_URL, headers=headers, json=payload)
#     ans = response.json()
#     return ans


#--------------whatsapp meta--------------------

# @csrf_exempt
# def whatsappwebhook(request):
#     if request.method == 'GET':
#         VERIFY_TOKEN = '1d731114-f447-4e87-b43e-8e858414ef95'
#         mode = request.GET['hub.mode']
#         token = request.GET['hub.verify_token']
#         challenge = request.GET['hub.challenge']
# 
#         if mode == "subscribe" and token == VERIFY_TOKEN:
#             return HttpResponse(challenge)
#         else:
#             return HttpResponse('error')
# 
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         print(data)
#         if 'object' in data and 'entry' in data:
#             try:
#                 for entry in data['entry']:
#                     phoneNumber = entry['changes'][0]['value']['metadata']['display_phone_number']
#                     phoneId = entry['changes'][0]['value']['metadata']['phone_number_id']
#                     profileName = entry['changes'][0]['value']['contacts'][0]['profile']['name']
#                     whatsAppId = entry['changes'][0]['value']['contacts'][0]['wa_id']
#                     fromId = entry['changes'][0]['value']['messages'][0]['from']
#                     messageId = entry['changes'][0]['value']['messages'][0]['id']
#                     timestamp = entry['changes'][0]['value']['messages'][0]['timestamp']
#                     text = entry['changes'][0]['value']['messages'][0]['text']['body']
# 
#                     # phoneNumber = "918149689641"
#                     message = "Hi, {}. Welcome to CollegeDekho.com services on whatsapp. How may i help you?".format(
#                         profileName)
#                     sendwhatsappmessages(fromId, message)
#             except:
#                 pass
#         return HttpResponse('success', status=200)

#----------------infobip---------
# @csrf_exempt
# def infobip(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         print(data)
#         if 'results' in data:
#             try:
#                 for i in data['results']:
#                     from_ = i['from']
#                     to = i['to']
#                     msg = i['message']['text']
#                     profile_name = i['contact']['name']
#                     mesage = 'Hi {}, Welcome to CollegeDekho.com services on whatsapp. How may i help you?'.format(
#                         profile_name)
#                     sendinfobipmessage(from_, mesage)
#             except:
#                 pass
#         return HttpResponse('success', status=200)

