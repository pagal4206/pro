from telebot import TeleBot
from Rudra import start
from config import *

bot = TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_handler(message):
    start.handle(bot, message)

@bot.callback_query_handler(func=lambda call: call.data == "check_joined")
def check_joined_handler(call):
    start.check_joined(bot, call)

if __name__ == "__main__":
    bot.infinity_polling()