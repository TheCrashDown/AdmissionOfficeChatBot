import telebot
import threading
from src.faqer import get_answer
from src.data_base_telegram import DataBaseTelegram
from src.data_base_monitor import DataBaseMonitor
import csv

from config.secret_config.TOKEN import TOKEN
from config.secret_config.DataBase import DB_NAME, DB_USER, DB_PASSWORD

bot = telebot.TeleBot(TOKEN)
data_base_telegram = DataBaseTelegram(DB_NAME, DB_USER, DB_PASSWORD)
data_base_monitor = DataBaseMonitor(DB_NAME, DB_USER, DB_PASSWORD)

keybord = telebot.types.ReplyKeyboardMarkup()
keybord.row("FAQ")
keybord.row("Test", "Monitoring")

@bot.message_handler(commands=['start'])
def start_message(message):
    data_base_telegram.add_user(message.chat.id)
    bot.send_message(message.chat.id, 'Hello World', reply_markup=keybord)


@bot.message_handler(commands=['help'])
@bot.message_handler(func=lambda message: message.text.lower() == 'help')
def start_message(message):
    with open("res/help_message.txt", "r") as f:
        bot.send_message(message.chat.id, f.read())


@bot.message_handler(commands=['faq'])
@bot.message_handler(func=lambda message: message.text.lower() == 'faq')
def faq_message(message):
    data_base_telegram.set_status(message.chat.id, "FAQ")
    bot.send_message(message.chat.id, 'Напишите ваше сообщение', reply_markup=telebot.types.ReplyKeyboardRemove())

@bot.message_handler(func=lambda message: data_base_telegram.get_status(message.chat.id) == "FAQ")
def faq_question(message):
    message_to_send = "Sorry, error happened"
    with open("data/queries.csv") as f:
        f_csv = csv.reader(f, delimiter='\t')
        i = 0
        needed_i = get_answer(message.text)
        for query in f_csv:
            if i == needed_i:
                message_to_send = query[1]
                break
            i += 1

    data_base_telegram.set_status(message.chat.id, "")
    bot.send_message(message.chat.id, message_to_send, parse_mode="HTML", reply_markup=keybord)


@bot.message_handler(commands=['test'])
@bot.message_handler(func=lambda message: message.text.lower() == 'test')
def test_message(message):
    bot.send_message(message.chat.id, 'Да что тут тестировать видно же что вы пидор')


@bot.message_handler(commands=['monitoring'])
@bot.message_handler(func=lambda message: message.text.lower() == 'monitoring')
def monitoring_message(message):
    print("---------------------monitor start")
    if data_base_telegram.get_email(message.chat.id) == None:
        bot.send_message(message.chat.id, "Чтобы увидеть свое место в рейтинге, укажите свой e-mail, чтобы мы поняли кто вы")
        email = get_message()
        print("---------------------")
        print(email)
        data_base_telegram.set_email(message.chat.id, email)
    bot.send_message(message.chat.id, 'Ваши шансы поступить стремятся к размеру вашего члена, сори как бы')


@bot.message_handler()
def get_message(message):
    return message



bot_thread = threading.Thread(target=bot.polling)
bot_thread.start()
