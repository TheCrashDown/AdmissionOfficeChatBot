import telebot
import threading
from src.Utility.faqer import get_answer
from src.data_base_telegram import DataBaseTelegram
from src.data_base_monitor import DataBaseMonitor
import csv

from config.secret_config.TOKEN import TOKEN
from config.secret_config.DataBase import DB_NAME, DB_USER, DB_PASSWORD

bot = telebot.TeleBot(TOKEN)
data_base_telegram = DataBaseTelegram(DB_NAME, DB_USER, DB_PASSWORD)
data_base_monitor = DataBaseMonitor(DB_NAME, DB_USER, DB_PASSWORD)

keybord = telebot.types.ReplyKeyboardMarkup()
keybord.row("FAQ", "Monitoring")


@bot.message_handler(commands=['start'])
def start_message(message):
    data_base_telegram.add_user(message.chat.id)
    with open("res/start_message.txt", "r") as f:
        bot.send_message(message.chat.id, f.read())


@bot.message_handler(commands=['help'])
@bot.message_handler(func=lambda message: message.text.lower() == 'help')
def start_message(message):
    with open("res/help_message.txt", "r") as f:
        bot.send_message(message.chat.id, f.read())


@bot.message_handler(commands=['login'])
def login_message(message):
    email = data_base_telegram.get_email(message.chat.id)
    if email is None:
        data_base_telegram.set_status(message.chat.id, "SEND_MAIL")
        bot.send_message(message.chat.id, "Укажите свой e-mail", reply_markup=telebot.types.ReplyKeyboardRemove())
        return
    bot.send_message(message.chat.id,
                     "Вы уже залогинились как " + email + ". Используйте команду /logout чтобы выйти из системы.")


@bot.message_handler(commands=['logout'])
def logout_message(message):
    email = data_base_telegram.get_email(message.chat.id)
    if email is None:
        bot.send_message(message.chat.id, "Вы не вошли в систему. Используйте команду /login чтобы сделать это.",
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        return
    data_base_telegram.set_email(message.chat.id, None)
    bot.send_message(message.chat.id, "Вы успешно разлогинились. Используйте команду /login, чтобы снова войти в систему.")


@bot.message_handler(commands=['faq'])
@bot.message_handler(func=lambda message: message.text.lower() == 'faq')
def faq_message(message):
    data_base_telegram.set_status(message.chat.id, "FAQ")
    bot.send_message(message.chat.id, 'Напишите ваше сообщение', reply_markup=telebot.types.ReplyKeyboardRemove())


@bot.message_handler(func=lambda message: data_base_telegram.get_status(message.chat.id) == "FAQ")
def faq_question(message):
    try:
        with open("data/queries.csv") as f:
            f_csv = csv.reader(f, delimiter='\t')
            i = 0
            needed_i = get_answer(message.text)
            for query in f_csv:
                if i in needed_i:
                    bot.send_message(message.chat.id, "Вопрос: " + str(query[0]) + "Ответ: " + str(query[1]), parse_mode="HTML", reply_markup=keybord)
                i += 1

        data_base_telegram.set_status(message.chat.id, "")
        bot.send_message(message.chat.id, 'Если вы не нашли нужный вам ответ, вы можете задать вопрос на <a href = "pk.mipt.ru/faq">сайте мфти</a>', parse_mode="HTML", reply_markup=keybord)
    except Exception:
        data_base_telegram.set_status(message.chat.id, "")
        bot.send_message(message.chat.id, 'Если вы не нашли нужный вам ответ, вы можете задать вопрос на <a href = "pk.mipt.ru/faq">сайте мфти</a>', parse_mode="HTML", reply_markup=keybord)


def monitoring(chat_id):
    ladder, number = data_base_monitor.receive_ladder(chat_id)

    str_to_send = 'Текущее состояние таблицы таково:\n<pre>\n.....................\n'

    for row in ladder:
        if row[0] == number:
            str_to_send += "> "
        else:
            str_to_send += "  "
        str_to_send += "{: >2} {: <15}{: <5}{}\n".format(row[0], row[2] + " " + row[1][0] + ".", row[3],
                                                                       "Ориг." if row[4] else "Копия")

    str_to_send += ".....................\n</pre>\n"

    bot.send_message(chat_id, str_to_send, reply_markup=keybord, parse_mode='HTML')

    your_summary = data_base_monitor.get_summary(chat_id)
    number_of_people = data_base_monitor.number_of_people()
    above = data_base_monitor.get_number_of_people_above(chat_id)
    above_ = data_base_monitor.get_number_of_people_above_with_certificate(chat_id)

    stats = ("У вас баллов: {0}\n"
             "Количество людей выше вас: {1}\n"
             "Количество людей выше вас, подавших оригинал аттестата: {2}\n"
             "Всего людей, подавших документы: {3}\n"
             "Проходной балл в прошлом году: 262").format(your_summary, above, above_, number_of_people)

    bot.send_message(chat_id, stats)


@bot.message_handler(commands=['monitoring'])
@bot.message_handler(func=lambda message: message.text.lower() == 'monitoring')
def monitoring_message(message):
    if data_base_telegram.get_email(message.chat.id) is None:
        data_base_telegram.set_status(message.chat.id, "SEND_MAIL")
        bot.send_message(message.chat.id, "Чтобы увидеть свое место в рейтинге, укажите свой e-mail",
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        return
    monitoring(message.chat.id)


@bot.message_handler(func=lambda message: data_base_telegram.get_status(message.chat.id) == "SEND_MAIL")
def set_mail(message):
    try:
        if data_base_telegram.set_email(message.chat.id, message.text):
            bot.send_message(message.chat.id, "Пользователя с такой почтой не существует")
            return
        data_base_telegram.set_status(message.chat.id, "")
        monitoring(message.chat.id)
    except Exception:
        bot.send_message(message.chat.id, "Пользователя с такой почтой не существует")
        data_base_telegram.set_status(message.chat.id, "")


bot_thread = threading.Thread(target=bot.polling)
bot_thread.start()
