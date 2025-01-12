from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import *

def handle(bot, message):
    chat_id = message.chat.id
    start_message = "Welcome to Rudra Bot! 🚀\n\nTo use this bot, you must join our channel first."
    keyboard = InlineKeyboardMarkup()
    join_button = InlineKeyboardButton("Join Channel", url=f"https://t.me/{CHANNEL_USERNAME}")
    joined_button = InlineKeyboardButton("I have Joined", callback_data="check_joined")
    keyboard.add(join_button)
    keyboard.add(joined_button)
    bot.send_message(chat_id, start_message, reply_markup=keyboard)

def check_joined(bot, call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    try:
        member_status = bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id).status
        if member_status in ['member', 'administrator', 'creator']:
            bot.send_message(chat_id, "Thank you for joining! 🎉 You can now use the bot features.")
        else:
            bot.send_message(chat_id, "You haven't joined the channel yet. Please join first!")
    except:
        bot.send_message(chat_id, "Error checking channel membership. Please make sure the channel is public.")
