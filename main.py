import telebot
from telebot import types
import db
import mail
import re

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
db.create_tables();
token = "491935642:AAH8bboAvOR4VwInhs0QzCoUPH8hxC7FHSY"
bot = telebot.TeleBot(token)


#find @auca in list
def fn(str):
    value = str[-8:]
    if(value == "@auca.kg"):
        return True
    return False
    

@bot.message_handler(content_types=["text"])
def handle_text(message):
    wait_list = []
    chat_id = message.chat.id
    text = message.text.rstrip()
    if(db.get_user(chat_id) == None):
        db.create_user(chat_id, False, "None")
    else:
        # Not verified
        if(not db.is_verified(chat_id)):
            curr_user = db.get_user(chat_id)
            if(text == curr_user[3]):
                db.update_user(chat_id, True, text, "None")
                bot.send_message(chat_id, "Your email is verified, enjoy your chat!")
            elif EMAIL_REGEX.match(text) and fn(text):
                bot.send_message(chat_id, "We send a verification code to " + text + ", please enter verication code.")
                code = mail.get_code()
                mail.send("Dear Sir/Madam,\n your verification code is " + code,text)
                db.update_user(chat_id, False, text, code)
            else:
                bot.send_message(chat_id, "It is not correct AUCA email, please send your @auca.kg email")
        # Verified EMAIL
        else:
            if(text == "start"):
                wait_list.append(chat_id);
            elif(text == "end"):
                db.remove_chat(chat_id)
            bot.send_message(chat_id, "Your email verified, use commands start, end, help")

bot.polling(none_stop=False, interval = 0)


'''

markup = types.ReplyKeyboardMarkup()
a = types.KeyboardButton('strat')
b = types.KeyboardButton('stop')
c = types.KeyboardButton('help')
markup.row(a,b,c)

'''