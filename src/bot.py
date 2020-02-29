import telebot

from config.secret_config.TOKEN import TOKEN

bot = telebot.TeleBot(TOKEN)

keybord = telebot.types.ReplyKeyboardMarkup()
keybord.row("FAQ")
keybord.row("Test", "Monitoring")

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Hello World')


if __name__ == '__main__':
    bot.polling()