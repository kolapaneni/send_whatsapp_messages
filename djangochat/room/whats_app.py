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

def upload_media_to_s3(file):
    s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                      region_name=settings.AWS_REGION)

    # bucket_name = 'first-new-bucket'
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    object_key = os.path.basename(file)

    if file.endswith('.jpg') or file.endswith('.jpeg'):
        content_type = 'image/jpeg'
    elif file.endswith('.png'):
        content_type = 'image/png'
    elif file.endswith('.pdf'):
        content_type = 'application/pdf'
    elif file.endswith('.docx'):
        content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    elif file.endswith('.doc'):
        content_type = 'application/msword'
    elif file.endswith('.txt'):
        content_type = 'text/plain'
    elif file.endswith('.mp4'):
        content_type = 'video/mp4'
    elif file.endswith('.3gpp'):
        content_type = 'video/3gpp'
    else:
        raise ValueError('Unsupported file type')

    file_path = file

    s3.upload_file(file_path, bucket_name, object_key, ExtraArgs={'ContentType': content_type})

    url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': object_key}, ExpiresIn=604800)

    print(url)
    return url

