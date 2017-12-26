import telebot
from telebot import types
import db
import mail
import re

#find @auca.kg in provided string
def findAucaSting(str):
    value = str[-8:]
    if(value == "@auca.kg"):
        return True
    return False

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
#db.drop_tables()
db.create_tables();
token = "491935642:AAH8bboAvOR4VwInhs0QzCoUPH8hxC7FHSY"
bot = telebot.TeleBot(token)
db.generate_random_questions()
#axilary list with status names
status = db.getStatusList()

@bot.message_handler(content_types=["text"])
def handle_text(message):
    chat_id = message.chat.id
    text = message.text.rstrip()
    print('xxxxxx',text)
    if(db.get_user(chat_id) == None):
        db.create_user(chat_id, False, "None")
        bot.send_message(chat_id, "Hello it is AUCA ROULLET, first please enter @auca.kg email")
    else:
        curr_user = db.get_user(chat_id)
        
        # Not verified
        if(not db.is_verified(chat_id)):
            if(text == curr_user.code):
                db.update_user(chat_id, True, text, status["passive"])
                bot.send_message(chat_id, "Your email is verified, press /start to begin chatting")
            #Check email and send verification code to user email    
            elif EMAIL_REGEX.match(text) and findAucaSting(text):
                bot.send_message(chat_id, "We send a verification code to " + text + ", please enter verication code.")
                code = mail.get_code()
                mail.send("Dear Sir/Madam,\n your verification code is " + code,text)
                db.update_user(chat_id, False, text, code)
            else:
                bot.send_message(chat_id, "It is not correct AUCA email, please send your @auca.kg email")
        # Verified EMAIL
        else:
            if(curr_user.code == status["select"]):
                #when user code is select, we store  
                second_chat_id = db.get_from_list(int(text) - 1)
                bot.send_message(chat_id, "You are in chat with another user, type something!")
                bot.send_message(second_chat_id, "You are in chat with another user, type something!")
                db.create_chat(chat_id, second_chat_id)
                db.update_user(chat_id, True, None, "Active")
            elif(curr_user.code == status["add_interest"]):
                db.update_interest(chat_id, text)
                db.update_user(chat_id, True, None, status["passive"])
                bot.send_message(chat_id, "Interest added! type /start to chat with random user, type /select to select from list")
            #Case when a user verified and already provided his/her interest 
            elif(curr_user.code == status["passive"]):
                print(2)
                #changes status grom PASIVE to WAIT
                if(text == "/start"):
                    ln = db.list_len()
                    if(ln == 0):
                        db.add_to_list(chat_id)
                        db.update_user(chat_id, True, None, status["wait"])
                        bot.send_message(chat_id, "Please wait until we find you a company!")
                    else:
                        #select first user from list
                        second_chat_id = db.get_from_list(0)
                        bot.send_message(chat_id, "You are in chat with another user, type something!")
                        bot.send_message(second_chat_id, "You are in chat with another user, type something!")
                        db.create_chat(chat_id, second_chat_id)
                        db.update_user(chat_id, True, None, status["active"])
                        db.update_user(second_chat_id, True, None, status["active"])
                #shows list of users with status WAIT
                elif(text == "/select"):
                    users = db.get_all_from_list();
                    if(len(users) == 0):
                        bot.send_message(chat_id, "No users active.")
                    else:
                        bot.send_message(chat_id, "Provide number, chose user from the list")
                        for elem in users:
                            bot.send_message(chat_id, str(elem[0]) + " - " + elem[4])
                            #when show list of all users in wait list then asign chat id to email
                            db.update_user(str(elem[1]), True, str(elem[1]), status["wait"])
                        db.update_user(chat_id, True, curr_user.email, status["select"])
                elif(text == "/update"):
                    db.update_user(chat_id, True, text, status["add_interest"])
                    bot.send_message(chat_id, "Please enter your interest, seperated with comma.")
                else:
                    bot.send_message(chat_id, "Type /start, to start chating")
            elif(curr_user.code == status["wait"]):
                bot.send_message(chat_id, "Please wait until we find you a company!")
            #Case when a user already in chat
            else:
                print(3)
                #get second user_id from existing chat
                second_chat_id = db.get_chat(chat_id)
                #remove chat and send apropriate messages to both users
                if(text == "/end"):
                    bot.send_message(second_chat_id, "Your company left chat, type /start to start again.")
                    bot.send_message(chat_id, "You left chat, type /start to start again.")
                    db.update_user(chat_id, True, text, status["passive"])
                    db.update_user(second_chat_id, True, text, status["passive"])
                    db.remove_chat(chat_id)
                #provide list of random questing in case user do not know what to ask from his/her company
                elif(text == "/help"):
                    values = db.get_questions()
                    bot.send_message(chat_id, "Some hints, enjoy you company")
                    for elem in values:
                        bot.send_message(chat_id, elem)
                #send provided text to another user
                else:
                    bot.send_message(second_chat_id, text)
                    db.create_response(text, chat_id, second_chat_id)
                
#keep connection
bot.polling(none_stop=False, interval = 0)