from telebot import TeleBot
from Rudra import start
from Rudra.start import buy_apk, invite_user, buy_paid_apk, broadcast, users_collection
from config import *

bot = TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_handler(message):
    start.handle(bot, message)

@bot.callback_query_handler(func=lambda call: call.data == "check_joined")
def check_joined_handler(call):
    start.check_joined(bot, call)

@bot.callback_query_handler(func=lambda call: call.data == "buy_apk")
def handle_buy_apk(call):
    # Call the buy_apk function and pass the bot and the callback
    buy_apk(bot, call)

@bot.message_handler(commands=["broadcast"])
def handle_broadcast(message):
    broadcast(message)

@bot.message_handler(commands=['user'])
def user_count(message):
    # Fetch user count from MongoDB
    total_users = users_collection.count_documents({})
    
    # Send the user count to the requester
    bot.send_message(message.chat.id, f"📊 Total number of users: {total_users}")

@bot.callback_query_handler(func=lambda call: call.data == "invite_user")
def handle_invite_user(call):
    # Call the invite_user function and pass the bot and the callback
    invite_user(bot, call)

@bot.callback_query_handler(func=lambda call: call.data == "buy_paid_apk")
def handle_buy_paid_apk(call):
    # Call the buy_paid_apk function and pass the bot and the callback
    buy_paid_apk(bot, call)

if __name__ == "__main__":
    bot.infinity_polling()
