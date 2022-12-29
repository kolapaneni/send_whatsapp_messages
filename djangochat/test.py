import json
import requests

try:
    payload = {
        "company-name": "CollegeDekho",
        "event-data": {
            "event-name": "CLD",
            "event-id": "2"
        },
        "parameters": {
            "phone-number": "+919849256029",
            "variables": ["Balu", "ThankYou"],
            "url-variable": "http://127.0.0.1:8000/room/message",
            "header": { 
                "link": "https://static-cse.canva.com/_next/static/assets/02_featureblock_photo-editor_w1260xh921_cb38143ec259533ed65369cee2c12c2dcae160e649f89b32c0acf94b598d4d3a.png",
             }
         }
    }

    url = "https://app.kwiqreply.io/v2.0/trigger_event?token=665ab736-26d3-4d7d-ba98-879a2e37db8e"

    payload = json.dumps(payload)
    # print(payload)

    response = requests.request("POST", url, data=payload, verify=True)
    rs = response.text
    # print(rs)
    json_data = json.loads(rs)
    print(json_data)

except Exception as e:
    print(e)