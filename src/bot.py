import telebot
import threading
from src.faqer import get_answer
from src.data_base_telegram import DataBaseTelegram

from config.secret_config.TOKEN import TOKEN
from config.secret_config.DataBase import DB_NAME, DB_USER, DB_PASSWORD

bot = telebot.TeleBot(TOKEN)
data_base_telegram = DataBaseTelegram(DB_NAME, DB_USER, DB_PASSWORD)

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
    bot.send_message(message.chat.id, 'ФАК еще не распирсили, ожидайте, но УРА')


@bot.message_handler(commands=['monitoring'])
@bot.message_handler(func=lambda message: message.text.lower() == 'monitoring')
def monitoring_message(message):
    bot.send_message(message.chat.id, 'Ваши шансы поступить стремятся к размеру вашего члена, сори как бы')


@bot.message_handler(commands=['test'])
@bot.message_handler(func=lambda message: message.text.lower() == 'test')
def test_message(message):
    print(data_base_telegram.get_status(message.chat.id))
    data_base_telegram.set_status(message.text)
    bot.send_message(message.chat.id, 'Да что тут тестировать видно же что вы пидор')


bot_thread = threading.Thread(target=bot.polling)
bot_thread.start()
