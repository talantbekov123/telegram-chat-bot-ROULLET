import telebot
from telebot import types
import db
import mail
import re

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
#db.drop_tables()
db.create_tables();
token = "491935642:AAH8bboAvOR4VwInhs0QzCoUPH8hxC7FHSY"
bot = telebot.TeleBot(token)

'''
db.create_question("Where do you want to travel?")
db.create_question("What dish do you like to eat?")
db.create_question("What subject do you like the most in AUCA?")
db.create_question("In what department do you study?")
db.create_question("How old are you?")
'''

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
        bot.send_message(chat_id, "Hello it is AUCA ROULLET, first please enter @auca.kg email")
    else:
        curr_user = db.get_user(chat_id)
        # Not verified
        if(not db.is_verified(chat_id)):
            if(text == curr_user[3]):
                db.update_user(chat_id, True, text, "Pasive")
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
            if(curr_user[3] == "Pasive"):
                if(text == "start"):
                    ln = db.list_len()
                    if(ln == 0):
                        db.add_to_list(chat_id)
                        db.update_user(chat_id, True, None, "Wait")
                        bot.send_message(chat_id, "Please wait until we find you a company!")
                    else:
                        second_chat_id = db.get_from_list()
                        bot.send_message(chat_id, "You are in chat with another user, type something!")
                        bot.send_message(second_chat_id, "You are in chat with another user, type something!")
                        db.create_chat(chat_id, second_chat_id)
                        db.update_user(chat_id, True, None, "Active")
                        db.update_user(second_chat_id, True, None, "Active")
                else:
                    bot.send_message(chat_id, "Type start, to start chating")
            elif(curr_user[3] == "Wait"):
                bot.send_message(chat_id, "Please wait until we find you a company!")
            else:
                second_chat_id = db.get_chat(chat_id)
                if(text == "end"):
                    bot.send_message(second_chat_id, "Your company left chat, type start to start again.")
                    bot.send_message(chat_id, "You left chat, type start to start again.")
                    db.update_user(chat_id, True, text, "Pasive")
                    db.update_user(second_chat_id, True, text, "Pasive")
                    db.remove_chat(chat_id)
                elif(text == "help"):
                    values = db.get_questions()
                    bot.send_message(chat_id, "Some hints, enjoy you company")
                    for elem in values:
                        bot.send_message(chat_id, elem)
                else:
                    bot.send_message(second_chat_id, text)
                    print("***",chat_id, second_chat_id)
                    db.create_response(text, chat_id, second_chat_id)
                

bot.polling(none_stop=False, interval = 0)


'''

markup = types.ReplyKeyboardMarkup()
a = types.KeyboardButton('strat')
b = types.KeyboardButton('stop')
c = types.KeyboardButton('help')
markup.row(a,b,c)

'''