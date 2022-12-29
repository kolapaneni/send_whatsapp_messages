import requests

from djangochat import settings


def sendwhatsappmessages(phonenumber, message):
    headers = {"Authorization": settings.WHATSAPP_TOKEN}
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": phonenumber,
        "type": "text",
        "text": {"body": message}
    }
    response = requests.post(settings.WHATSAPP_URL, headers=headers, json=payload)
    ans = response.json()
    return ans

