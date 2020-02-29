import telebot
import threading
from src.faqer import get_answer
from src.data_base_telegram import DataBaseTelegram
from src.data_base_monitor import DataBaseMonitor
import csv

from config.secret_config.TOKEN import TOKEN
from config.secret_config.DataBase import DB_NAME, DB_USER, DB_PASSWORD

@bot.message_handler(commands=['monitoring'])
@bot.message_handler(func=lambda message: message.text.lower() == 'monitoring')
def monitoring_message(message):
    if data_base_monitor.check_user(message.chat.id) == 0:
        bot.send_message(message.chat.id, "Чтобы увидеть свое место в рейтинге, укажите свой e-mail, чтобы мы поняли кто вы")
        email = get_message()
        data_base_monitor.reg_user(message.chat.id, email)
    bot.send_message(message.chat.id, 'Ваши шансы поступить стремятся к размеру вашего члена, сори как бы')

@bot.message_handler()
def get_message(message):
    return message