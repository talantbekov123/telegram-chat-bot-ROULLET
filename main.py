import telebot
import db
db.drop_tables()
db.create_tables();
token = "491935642:AAH8bboAvOR4VwInhs0QzCoUPH8hxC7FHSY"
bot = telebot.TeleBot(token)


db.create_question("some data");
db.create_question("A");
db.create_question("B");
db.create_question("V");
db.create_question("C");
db.create_question("D");

db.show_questions();
db.get_questions()

'''
@bot.message_handler(content_types=["text"])
def handle_text(message):
    if(db.isVerified(message.chat.id))
        db.create_user(message.chat.id, False, "None")
        
    db.update_user(message.chat.id, True, "Hello")
    print("F2",db.isVerified(message.chat.id))

    db.show_users()
    bot.send_message(message.chat.id, "AUCA response")

bot.polling(none_stop=False, interval = 0)
'''