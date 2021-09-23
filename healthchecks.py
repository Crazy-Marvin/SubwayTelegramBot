import requests, time, os

# maybe the schedule module (https://schedule.readthedocs.io/en/stable/) would be nice too 🤔

API_KEY = os.getenv("API_KEY")
ID = os.getenv("ID")
MSG = ""

url = 'https://api.telegram.org/bot' + API_KEY + '/sendMessage?chat_id=' + ID + '&parse_mode=Markdown&text='
   
def main():

    global MSG

    while True:

        # Subway Telegram Bot
        try:
            requests.get(os.getenv("SUBWAY URL"), timeout=30)
            MSG += "SUBWAY BOT 🟢\n\n"
        except:
            MSG += "SUBWAY BOT 🔴\n\n"

        # YogiBot Telegram Bot
        try:
            requests.get(os.getenv("YOGI URL"), timeout=30)
            MSG += "YOGI BOT 🟢\n\n"
        except:
            MSG += "YOGI BOT 🔴\n\n"

        # Product Hunt Telegram Bot
        try:
            requests.get(os.getenv("PRODUCT HUNT URL"), timeout=30)
            MSG += "PRODUCT HUNT BOT 🟢\n\n"
        except:
            MSG += "PRODUCT HUNT BOT 🔴\n\n"

        # Funny Telegram Bot
        try:
            requests.get(os.getenv("FUNNY URL"), timeout=30)
            MSG += "FUNNY BOT 🟢\n\n"
        except:
            MSG += "FUNNY BOT 🔴\n\n"
            
        # YouTube Statistics Telegram Bot
        try:
            requests.get(os.getenv("YOUTUBE STATISTIS URL"), timeout=30)
            MSG += "YOUTUBE STATISTICS BOT 🟢\n\n"
        except:
            MSG += "YOUTUBE STATISTICS BOT 🔴\n\n"

        # Party Telegram Bot
        try:
            requests.get(os.getenv("PARTY URL"), timeout=30)
            MSG += "PARTY BOT 🟢\n\n"
        except:
            MSG += "PARTY BOT 🔴\n\n"

        requests.get(url=(url+MSG))
        MSG = ""
        time.sleep(3600)
