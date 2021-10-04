import requests
import os
import time

API_KEY = os.getenv("HEALTH_BOT_API")
ID = os.getenv("GROUP_ID")
MSG = ""

url = 'https://api.telegram.org/bot' + API_KEY + \
    '/sendMessage?chat_id=' + ID + '&parse_mode=Markdown&text='

while True:

    # Subway Telegram Bot
    try:
        requests.get(
            "https://hc-ping.com/db037b86-718a-4ce1-aecc-70e0a994965e", timeout=30)
        MSG += "🟢 SUBWAY BOT\n\n"
    except:
        MSG += "🔴 SUBWAY BOT\n\n"

    requests.get(url=(url+MSG))
    MSG = ""
    time.sleep(3600)