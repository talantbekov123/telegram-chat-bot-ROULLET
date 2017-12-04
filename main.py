import telebot
import db
db.drop_tables();
db.create_tables();
db.create_user(123,False,"talantbekov_k@auca.kg")
print("XX",db.find_user(123))
'''
token = "491935642:AAH8bboAvOR4VwInhs0QzCoUPH8hxC7FHSY"
bot = telebot.TeleBot(token)

@bot.message_handler(content_types=["text"])
def handle_text(message):
    print(message.chat.id)
    db.create_tables()
    temp = db.find_user(message.chat.id)
    print(temp)
    bot.send_message(message.chat.id, "AUCA response")

bot.polling(none_stop=False, interval = 0)
'''