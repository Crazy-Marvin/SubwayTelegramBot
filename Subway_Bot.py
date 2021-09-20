import telebot, dotenv, os, requests, gspread
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from oauth2client.service_account import ServiceAccountCredentials

dotenv.load_dotenv()

API_KEY = os.getenv("API_KEY") # your Token from @Botfather
my_id = os.getenv("my_id") # your personal chat ID
analyst_id = os.getenv("analyst_id") # your analyst chat ID
creds_location = os.getenv("creds_location")
forms_url = os.getenv("forms_url")  # your URL to the Google Forms for feedback
spreadsheet_url = os.getenv("spreadsheet_url") # your URL to the Google Spreadsheet for analytics

welcome_stk = "CAACAgIAAxkBAAN6YQg3tT0d6WxU_lo-bUquFOv0Qh8AAgUAA8A2TxP5al-agmtNdSAE"
thanks_stk = "CAACAgIAAxkBAAM_YQgjN81oKkVQl3LNKKt69sddvbwAAhcAA1m7_CX7oZ-xASU7NiAE"
menu_id = "AgACAgUAAxkBAAM7YT2p9MIaukb8Ksuop9cfgWThrKYAAkOtMRuI8PFV93Bu8V-r0rUBAAMCAAN5AAMgBA"
umm_stk = "CAACAgIAAxkBAAICnmEQKKxDZSnxXTsNn78JP93DbEMRAAKGCQACGELuCERh0dPDHzthIAQ"

# upload the images directly to Telegram and get the file_id via https://api.telegram.org/botYOURTOKEN/getUpdates
sub_of_the_day = {

'MONDAY': "AgACAgQAAxkBAAMIYT38MjRg8wvHWwMGkuCmtdDZtHIAAli4MRuw7_BR0qM12SzEdDABAAMCAANzAAMgBA",
'MONTAG': "AgACAgQAAxkBAAMIYT38MjRg8wvHWwMGkuCmtdDZtHIAAli4MRuw7_BR0qM12SzEdDABAAMCAANzAAMgBA",
'সোমবার': "AgACAgQAAxkBAAMIYT38MjRg8wvHWwMGkuCmtdDZtHIAAli4MRuw7_BR0qM12SzEdDABAAMCAANzAAMgBA",
'TUESDAY': "AgACAgQAAxkBAAMaYT39sVA66cFuSzFp9hHcvRGPft4AAl24MRuw7_BR_FupQGj6ny4BAAMCAANzAAMgBA",
'DIENSTAG': "AgACAgQAAxkBAAMaYT39sVA66cFuSzFp9hHcvRGPft4AAl24MRuw7_BR_FupQGj6ny4BAAMCAANzAAMgBA",
'মঙ্গলবার': "AgACAgQAAxkBAAMaYT39sVA66cFuSzFp9hHcvRGPft4AAl24MRuw7_BR_FupQGj6ny4BAAMCAANzAAMgBA",
'WEDNESDAY': "AgACAgQAAxkBAAMbYT3979L9L0BQP67uEuQLMZV2GlgAAl64MRuw7_BRXj_0gTKrrTsBAAMCAANzAAMgBA",
'MITTWOCH': "AgACAgQAAxkBAAMbYT3979L9L0BQP67uEuQLMZV2GlgAAl64MRuw7_BRXj_0gTKrrTsBAAMCAANzAAMgBA",
'বুধবা': "AgACAgQAAxkBAAMbYT3979L9L0BQP67uEuQLMZV2GlgAAl64MRuw7_BRXj_0gTKrrTsBAAMCAANzAAMgBA",
'THURSDAY': "AgACAgQAAxkBAAMcYT3-OymmPW3980xNHpI8hA7LemMAAl-4MRuw7_BRlFCUon1EIHcBAAMCAANzAAMgBA",
'DONNERSTAG': "AgACAgQAAxkBAAMcYT3-OymmPW3980xNHpI8hA7LemMAAl-4MRuw7_BRlFCUon1EIHcBAAMCAANzAAMgBA",
'বৃহস্পতিবার': "AgACAgQAAxkBAAMcYT3-OymmPW3980xNHpI8hA7LemMAAl-4MRuw7_BRlFCUon1EIHcBAAMCAANzAAMgBA",
'FRIDAY': "AgACAgQAAxkBAAMdYT3-aJbDq-ze9zIzDwFjho3tafkAAmC4MRuw7_BR76ppExZyOzABAAMCAANzAAMgBA",
'FREITAG': "AgACAgQAAxkBAAMdYT3-aJbDq-ze9zIzDwFjho3tafkAAmC4MRuw7_BR76ppExZyOzABAAMCAANzAAMgBA",
'শুক্রবার': "AgACAgQAAxkBAAMdYT3-aJbDq-ze9zIzDwFjho3tafkAAmC4MRuw7_BR76ppExZyOzABAAMCAANzAAMgBA",
'SATURDAY': "AgACAgQAAxkBAAMeYT3-leDklyigPmrYGgYlvo_Bks4AAmG4MRuw7_BRhg2yh1bkzqQBAAMCAANzAAMgBA",
'SAMSTAG': "AgACAgQAAxkBAAMeYT3-leDklyigPmrYGgYlvo_Bks4AAmG4MRuw7_BRhg2yh1bkzqQBAAMCAANzAAMgBA",
'শনিবার': "AgACAgQAAxkBAAMeYT3-leDklyigPmrYGgYlvo_Bks4AAmG4MRuw7_BRhg2yh1bkzqQBAAMCAANzAAMgBA",
'SUNDAY': "AgACAgQAAxkBAAMfYT3-wkdKB72DYJOeISROuxwR7QMAAmK4MRuw7_BR2S2mNfvujVYBAAMCAANzAAMgBA",
'SONNTAG': "AgACAgQAAxkBAAMfYT3-wkdKB72DYJOeISROuxwR7QMAAmK4MRuw7_BR2S2mNfvujVYBAAMCAANzAAMgBA",
'রবিবার': "AgACAgQAAxkBAAMfYT3-wkdKB72DYJOeISROuxwR7QMAAmK4MRuw7_BR2S2mNfvujVYBAAMCAANzAAMgBA",
}

day_commands = ['monday', 'montag', 'সোমবার', 'tuesday', 'dienstag', 'মঙ্গলবার', 'wednesday', 'mittwoch', 'বুধবা', 'thursday', 'donnerstag', 'বৃহস্পতিবার', 'friday', 'freitag', 'শুক্রবার', 'saturday', 'samstag', 'শনিবার', 'sunday', 'sonntag', 'রবিবার']

subway_bot = telebot.TeleBot(API_KEY)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
"https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

analytics_SUBWAY_BOT = client.open("ANALYTICS").worksheet("SUBWAY_BOT")
database = client.open("SUBWAY BOT DATABASE").worksheet("DATABASE")

@subway_bot.message_handler(commands=['start'])
def send_hello(message):

    col = database.col_values(1)

    if str(message.chat.id) not in col:
        database.append_row([message.chat.id])
        analytics_SUBWAY_BOT.update_acell('F10', str(len(database.col_values(1))).replace("'"," "))

    mark_up = InlineKeyboardMarkup()
    B1 = InlineKeyboardButton(text='SUB OF THE DAY!', callback_data = 'sub')
    B2 = InlineKeyboardButton(text='MENU', url= 'https://www.subway.com/de-DE/MenuNutrition/Menu/Sub-of-the-Day')
    B3 = InlineKeyboardButton(text='FEEDBACK', url="https://forms.gle/UnS4hcFamKmDsAKL8")
    B4 = InlineKeyboardButton(text='CONTACT', callback_data='contact')

    mark_up.row(B1,B2)
    mark_up.row(B3,B4)

    subway_bot.send_sticker(message.chat.id, welcome_stk, reply_markup=mark_up)
    start_count = analytics_SUBWAY_BOT.acell('F3').value
    analytics_SUBWAY_BOT.update_acell('F3',str(int(start_count)+1).replace("'"," "))

@subway_bot.message_handler(commands=['sub'])
def sub(message):

    from datetime import date
    from calendar import day_name

    day = day_name[date.today().weekday()].upper()
    subway_bot.send_message(message.chat.id,"Check out the *SUB OF THE DAY\! 😋👇🏻*",parse_mode='MarkdownV2')
    sub = sub_of_the_day[day]
    subway_bot.send_photo(message.chat.id, sub)
    sub_count = analytics_SUBWAY_BOT.acell('F4').value
    analytics_SUBWAY_BOT.update_acell('F4',str(int(sub_count)+1).replace("'"," "))

@subway_bot.message_handler(commands=['menu'])
def menu(message):

    subway_bot.send_photo(message.chat.id, menu_id)
    subway_bot.send_message(message.chat.id, "For more details visit: *[SUBWAY GERMANY]\
(https://www.subway.com/de-DE/MenuNutrition/Menu/Sub-of-the-Day)*", parse_mode='MarkdownV2', disable_web_page_preview=True)
    menu_count = analytics_SUBWAY_BOT.acell('F5').value
    analytics_SUBWAY_BOT.update_acell('F5',str(int(menu_count)+1).replace("'"," "))

@subway_bot.message_handler(commands=['contact'])
def contact(message):
    contact_info = '''
*CONTACT :*\n
Telegram: https://t\.me/Marvin\_Marvin\n
Mail: marvin@poopjournal\.rocks\n
Issue: https://github\.com/Crazy\-Marvin/SubwayTelegramBot/issues\n
Source: https://github\.com/Crazy\-Marvin/SubwayTelegramBot
'''
    subway_bot.send_message(message.chat.id, contact_info,parse_mode='MarkdownV2')
    contact_count = analytics_SUBWAY_BOT.acell('F6').value
    analytics_SUBWAY_BOT.update_acell('F6',str(int(contact_count)+1).replace("'"," "))

@subway_bot.message_handler(commands=['feedback'])
def feedback(message):

    subway_bot.send_message(message.chat.id,"Want to give us a feedback?\n\n\
{forms_url} \n\nPlease fill out this Google Form☝🏻")
    subway_bot.send_sticker(message.chat.id, thanks_stk)
    feedback_count = analytics_SUBWAY_BOT.acell('F7').value
    analytics_SUBWAY_BOT.update_acell('F7',str(int(feedback_count)+1).replace("'"," "))

@subway_bot.message_handler(commands=['logs'])
def logs(message):

    if message.chat.id == os.getenv('my_id') or message.chat.id == os.getenv('analyst_id'):
        spreadsheet_url = os.getenv('spreadsheet_url')  # spreadsheet url
        subway_bot.send_message(message.chat.id, f"Check out the *[ANALYTICS]({spreadsheet_url})* for the month\.",parse_mode="MarkdownV2",disable_web_page_preview=True)

@subway_bot.message_handler(content_types='text')
def day(message):
    if (message.text).lower() in day_commands:
        sub = sub_of_the_day[(message.text).upper()]
        subway_bot.send_photo(message.chat.id,sub)
        sub_count = analytics_SUBWAY_BOT.acell('F4').value
        analytics_SUBWAY_BOT.update_acell('F4',str(int(sub_count)+1).replace("'"," "))
    else:
        subway_bot.send_message(message.chat.id, "Umm...I really don't know how to respond to this message.")
        subway_bot.send_sticker(message.chat.id, umm_stk)

        if message.chat.id != int(my_id):
            subway_bot.send_message(my_id, "Hey! Someone just sent me something that I don't understand...")
            subway_bot.send_message(my_id, f"Sender Details:\
\nName: {message.from_user.first_name} {message.from_user.last_name}.\
\nUser Id: @{message.from_user.username}\
\nChat Id: {message.chat.id}\
\nMessage Id: {message.id}")
            subway_bot.forward_message(my_id, message.chat.id, message.id)

types = ['audio', 'document', 'photo', 'sticker', 'video', 'video_note', 'voice',
         'location', 'contact', 'new_chat_members', 'left_chat_member', 'new_chat_title',
          'new_chat_photo', 'delete_chat_photo', 'group_chat_created', 'supergroup_chat_created', 
          'channel_chat_created', 'migrate_to_chat_id', 'migrate_from_chat_id', 'pinned_message']

@subway_bot.message_handler(content_types=types)
def rubbish(message):

    subway_bot.send_message(message.chat.id, "Umm...I really don't know how to respond to this message.")
    subway_bot.send_sticker(message.chat.id, umm_stk)

    if message.chat.id != int(my_id):
        subway_bot.send_message(my_id, "Hey! Someone just sent me something that I don't understand...")
        subway_bot.send_message(my_id, f"Sender Details:\
\nName: {message.from_user.first_name} {message.from_user.last_name}.\
\nUser Id: @{message.from_user.username}\
\nChat Id: {message.chat.id}\
\nMessage Id: {message.id}")
        subway_bot.forward_message(my_id, message.chat.id, message.id)

@subway_bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):

    data = call.data
    if data == 'sub':
        sub(call.message)
    elif data == 'contact':
        contact(call.message)

subway_bot.polling() # checking for new messages
