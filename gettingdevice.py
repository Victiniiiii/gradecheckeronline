import requests

PUSHBULLET_API_KEY = "Please enter your api key here: "

response = requests.get(
    'https://api.pushbullet.com/v2/devices',
    headers={'Access-Token': PUSHBULLET_API_KEY}
)

if response.status_code == 200:
    devices = response.json()['devices']
    for device in devices:
        print(f"Device Nickname: {device['nickname']}, Device Iden: {device['iden']}")
else:
    print("Failed to retrieve devices")
