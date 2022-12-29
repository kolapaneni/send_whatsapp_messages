from django.http import HttpResponse
from rest_framework.decorators import api_view, renderer_classes
from twilio.twiml.messaging_response import MessagingResponse
from rest_framework.renderers import JSONRenderer

"""
The first thing we need to do in our chatbot is obtain the message entered by the user. This message comes in the payload of the POST request with a key of ’Body’. We can access it through Django’s request object:
"""


@api_view(['POST'])
@renderer_classes([JSONRenderer])
def whatsAppmsg(request):
    incoming_msg = request.data['Body'].lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if incoming_msg:

        # change below code for automated response

        if 'hi' in incoming_msg:
            quote = 'Hello'
            msg.to(quote)
            msg.body(quote)
            responded = True
        if "how are you" in incoming_msg:
            quote = "I'm good. How are you"
            msg.body(quote)
            responded = True
        if "colleges" in incoming_msg:
            quote = "Go to this link https://www.google.com/search?gs_ssp" \
                    "=eJzj4tVP1zc0TDY1To6vMi8wYLRSNagwtjRIMbQ0SkwySTRKNLI0tzKoMDc2Mk9LtDROTDZMTjFNM_PiSc7PyUlNT01Jzc7IBwCCURP_&q=collegedekho&oq=collegedek&aqs=chrome.2.69i65j69i57j46i175i199i433i512j0i512j69i65j69i60l3.7526j0j7&sourceid=chrome&ie=UTF-8 "
            msg.body(quote)
            responded = True
        if 'order' in incoming_msg:
            quote = 'order details'
            msg.body(quote)
            # return a cat pic
            # msg.media('https://cataas.com/cat')
            responded = True
    if not responded:
        msg.body('Sorry! Give Some message.')
    return HttpResponse(str(resp))