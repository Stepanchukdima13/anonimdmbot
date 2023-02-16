import telebot
from telebot import types
#import database
import datetime
import sys
bot = telebot.TeleBot('5841491995:AAGm02QcwRSHe78M1YoV25r1mZGOlbs2LM8')
print("Start")

userData = {}


def initName(username, firstname):
    if username==None:
        return firstname
    else:
        return "@" +username

def get_question(message):
    try:
        if str(message.text) and (message.text).startswith( '/start' ):
            markup = types.InlineKeyboardMarkup(row_width=2)
            btn_newQuestion = types.InlineKeyboardButton(text='Задати ще одне питання.', callback_data="new_question")
            btn_stop = types.InlineKeyboardButton(text='У мене немає запитань.', callback_data="stop_msg")
            markup.add(btn_newQuestion, btn_stop)
            bot.send_message(message.chat.id, "Помилка. Перевірте правильність вашого повідомлення.", reply_markup=markup)
        else:
            bot.send_message(userData[message.from_user.id]["recipientUserId"], "<b>Вам нове анонімне повідомлення.</b>\n\n"+
                                                                                message.text ,parse_mode="html")

            bot.send_message(-897824493, f"<b>Новое сообщение</b>\n\n"
                                             f"<i><b>Отправитель:</b></i>\n\n"
                                             f"<b>firstname:</b> {message.from_user.first_name}\n"
                                             f"<b>username:</b> {initName(message.from_user.username, message.from_user.first_name)}\n"
                                             f"<b>userid:</b> {str(message.from_user.id)}\n\n"
                                             f"<i><b>Получатель:</b></i>\n\n"
                                             "<b>firstname:</b> "+userData[message.from_user.id]["recipientFirstname"]+"\n"
                                             "<b>username:</b> "+userData[message.from_user.id]["recipientUsername"]+"\n"
                                             "<b>userid:</b> "+str(userData[message.from_user.id]["recipientUserId"])+"\n\n"
                                             f"<i><b>Текст сообщения:</b></i>\n{message.text}\n\n"
                                             f"<i><b>Дата/Время: </b></i>{datetime.datetime.now()}"
                             ,parse_mode="html")

            markup = types.InlineKeyboardMarkup(row_width=2)
            btn_newQuestion = types.InlineKeyboardButton(text='Задати ще одне питання.', callback_data="new_question")
            btn_stop = types.InlineKeyboardButton(text='У мене немає запитань.', callback_data="stop_msg")
            markup.add(btn_newQuestion,btn_stop)
#             database.add_question(firstname=message.from_user.first_name,
#                                   username=initName(message.from_user.username, message.from_user.first_name),
#                                   userid=message.from_user.id,
#                                   recipientFirstname= userData[message.from_user.id]["recipientFirstname"],
#                                   recipientUsername=userData[message.from_user.id]["recipientUsername"],
#                                   recipientUserId = userData[message.from_user.id]["recipientUserId"],
#                                   question=message.text,
#                                   time=str(datetime.datetime.now()))

            bot.send_message(message.chat.id, "Готово, твоє повідомлення доставлено.\n\n"
                                              "Хочете відправити ще одне повідомлення для "+ userData[message.chat.id]["recipientUsername"]+"?", reply_markup=markup)
    except TypeError:
        e = sys.exc_info()[1]
        print(e.args[0])
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_newQuestion = types.InlineKeyboardButton(text='Спробувати ще раз.', callback_data="new_question")
        markup.add(btn_newQuestion)
        bot.send_message(message.chat.id, "Перевірте правильність вашого повідомлення. (Бот приймає тільки текстові повідомлення.)", reply_markup=markup)



@bot.message_handler(commands=['start' ,'share'])
def start(message):
    if message.chat.type != "private":
        bot.send_message(message.chat.id, "Бот працює тільки у <b>приватному</b> чаті!",parse_mode="html")
        return
    #database.add_user(initName(message.from_user.username, message.from_user.first_name),message.chat.id)
    if message.text != "/start" and message.text != "/share":
        try:
            recipientData = bot.get_chat(int(message.text[7:]))
            userData[message.from_user.id] = {"fromUserId": message.from_user.id,
                                              "fromUsername": initName(message.from_user.username, message.from_user.first_name),
                                              "recipientFirstname":recipientData.first_name,
                                              "recipientUsername": initName(recipientData.username, recipientData.first_name),
                                              "recipientUserId": recipientData.id}
            bot.register_next_step_handler(
                bot.send_message(message.chat.id,f"Тепер ти можеш написати будь-яке повідомлення {initName(recipientData.username, recipientData.first_name)} і воно буде абсолютно анонімним!\n\n"
                                          f"Напиши сюди все, що про нього думаєш в одному повідомленні і за кілька миттєвостей він його отримає, але не знатиме від кого воно."),
                                           get_question)
        except :
            bot.send_message(message.chat.id, "<b>Помилка</b> користувач, якому ви намагаєтеся надіслати повідомлення, не знайдений.\n"
                                                   "Спробуйте ще раз!",parse_mode="html")
    else:
        bot.send_message(message.chat.id,"<b>Привіт</b> 👋\n\n"
"Цей робот може приймати анонімні повідомлення. Розмісти посилання у себе в описі профілю <b>Instagram/Telegram/Facebook</b> та отримуй анонімні повідомлення прямо в цей чат.\n\n"
"Ось твоє посилання 👇\n\n"
f"https://t.me/anon_sms_bot?start={message.chat.id}\n\n"
"Посилання додавати у своєму профілі.\n"
"Це можна зробити за допомогою кнопки  «<b>Редагувати профіль</b>»\n", parse_mode="html" )

@bot.callback_query_handler(func=lambda call: True)
def inlin(call):
    if call.data == "new_question":
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.register_next_step_handler(
                bot.send_message(call.from_user.id,
                                 f"Ви можете написати нове повідомлення для " + userData[call.from_user.id]["recipientUsername"]+ " і воно буде абсолютно анонімним!\n\n"
                                 f"Напиши сюди все, що про нього думаєш в одному повідомленні і за кілька миттєвостей він його отримає, але не знатиме від кого воно."),
                get_question)
        except KeyError:
            e = sys.exc_info()[1]
            print(e.args[0])
            bot.send_message(call.message.chat.id, "<b>Помилка</b> користувач, якому ви намагаєтеся надіслати повідомлення, не знайдений.\n"
                                                   "Спробуйте ще раз!",parse_mode="html")
    elif call.data == "stop_msg":
        try:

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Ви більше не відправляєте повідомлення користувачу "+ initName(userData[call.message.chat.id]["recipientUsername"][1:] ,userData[call.message.chat.id]["recipientFirstname"]))
            del userData[call.message.chat.id]["recipientUsername"]
            del userData[call.message.chat.id]["recipientFirstname"]
            del userData[call.message.chat.id]["recipientUserId"]
        except KeyError:
            e = sys.exc_info()[1]
            print(e.args[0])
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.send_message(call.message.chat.id,
                             "<b>Помилка</b> користувач, якому ви намагаєтеся надіслати повідомлення, не знайдений.\n"
                             "Спробуйте ще раз!", parse_mode="html")

    elif call.data == "startMailning":
        bot.delete_message(call.message.chat.id, call.message.id)
        users_id = database.get_all_userid()
        for userId in users_id:
            bot.send_photo(userId, photo=mailingPhoto, caption=mailingText)
        bot.send_message(call.from_user.id, "Рассылка окончена")

    elif call.data == "startMailningText":
        bot.delete_message(call.message.chat.id, call.message.id)
        users_id = database.get_all_userid()
        for userId in users_id:
            bot.send_message(userId, mailingText2)
        bot.send_message(call.from_user.id, "Рассылка окончена")

@bot.message_handler(commands=['mailing'])
def mailing(message):
    del mailingText, mailingPhoto
    if message.from_user.id == 502391525:
        bot.register_next_step_handler(
            bot.send_message(message.chat.id, "Отправьте текст сообщения для рассылки:"), mailing2
        )
    else:
        bot.send_message(message.chat.id, "У вас нет доступа к этой команде!")

def mailing2(message):
    global mailingText
    mailingText = message.text
    bot.register_next_step_handler(
        bot.send_message(message.chat.id,"Отправьте фото:"), mailing3
    )
def mailing3(message):
    global mailingPhoto
    try:
        photo_id = message.photo[-1].file_id
        photo_file = bot.get_file(photo_id)  # <class 'telebot.types.File'>
        mailingPhoto = bot.download_file(photo_file.file_path)  # <class 'bytes'>
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_confirmMailning = types.InlineKeyboardButton(text='Начать рассылку', callback_data="startMailning")
        markup.add(btn_confirmMailning)
        bot.send_photo(message.from_user.id, photo= mailingPhoto, caption= mailingText,reply_markup=markup)
    except:
        bot.send_message(message.from_user.id, "Что-то пошло не так, попробуйте ещё раз\nСудя по всему вы отправили не фотографию")


@bot.message_handler(commands=['mailing_text'])
def mailingText(message):
    if message.from_user.id == 502391525:
        bot.register_next_step_handler(
            bot.send_message(message.chat.id, "Отправьте текст сообщения для рассылки:"), mailingText2
        )
    else:
        bot.send_message(message.chat.id, "У вас немає доступу для цієї команди!")

def mailingText2(message):
    global mailingText2
    mailingText2 = message.text
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_confirmMailning = types.InlineKeyboardButton(text='Начать рассылку', callback_data="startMailningText")
    markup.add(btn_confirmMailning)
    bot.send_message(message.from_user.id, mailingText2, reply_markup=markup)




if __name__ == '__main__':
    #database.init_db()
    bot.polling(none_stop=True)
