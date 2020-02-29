import telebot
import threading

from config.secret_config.TOKEN import TOKEN

bot = telebot.TeleBot(TOKEN)

keybord = telebot.types.ReplyKeyboardMarkup()
keybord.row("FAQ")
keybord.row("Test", "Monitoring")

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Hello World', reply_markup=keybord)


@bot.message_handler(commands=['help'])
def start_message(message):
    with open("res/help_message.txt", "r") as f:
        bot.send_message(message.chat.id, f.read())

@bot.message_handler(commands=['faq'])
def faq_message(message):
    bot.send_message(message.chat.id, 'ФАК еще не распирсили, ожидайте')


@bot.message_handler(commands=['monitoring'])
def monitoring_message(message):
    bot.send_message(message.chat.id, 'Ваши шансы поступить стремятся к размеру вашего члена, сори как бы')


@bot.message_handler(commands=['test'])
def test_message(message):
    bot.send_message(message.chat.id, 'Да что тут тестировать видно же что вы пидор')


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'faq':
        bot.send_message(message.chat.id, 'ФАК еще не распирсили, ожидайте')
    elif message.text.lower() == 'monitoring':
        bot.send_message(message.chat.id, 'Ваши шансы поступить стремятся к размеру вашего члена, сори как бы')
    elif message.text.lower() == 'test':
        bot.send_message(message.chat.id, 'Да что тут тестировать видно же что вы пидор')



bot_thread = threading.Thread(target=bot.polling)
bot_thread.start()
