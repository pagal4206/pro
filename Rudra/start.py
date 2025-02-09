import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
from config import *  # Bot token, MongoDB URL, etc.
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot(BOT_TOKEN)

# MongoDB connection
client = MongoClient(MONGO_URL)
db = client["telegram_bot"]
users_collection = db["users"]

# Handle incoming messages
def handle(bot, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    referrer_id = None

    if len(message.text.split()) > 1:
        referrer_id = message.text.split()[1]

    user = users_collection.find_one({"user_id": user_id})
    
    if not user:
        new_user = {"user_id": user_id, "points": 0, "referred_by": referrer_id}
        users_collection.insert_one(new_user)
        user = new_user
        
        if referrer_id:
            referrer = users_collection.find_one({"user_id": int(referrer_id)})
            if referrer:
                users_collection.update_one({"user_id": int(referrer_id)}, {"$inc": {"points": 1}})
                referrer_username = message.from_user.username or message.from_user.first_name
                referrer_message = f"🎉 **{referrer_username}** has successfully referred a new user!\n✨ {message.from_user.username} started the bot and earned 1 coin!"
                bot.send_message(int(referrer_id), referrer_message, parse_mode="Markdown")
    else:
        if referrer_id:
            referrer = users_collection.find_one({"user_id": int(referrer_id)})
            if referrer:
                referrer_username = message.from_user.username or message.from_user.first_name
                referrer_message = f"⚠️ **{referrer_username}** has already joined using your referral link.\n🔁 Please send the link to other users to earn coins."
                bot.send_message(int(referrer_id), referrer_message, parse_mode="Markdown")

    points = user.get('points', 0)
    start_message = f"""
    👑 𝐎𝐊 𝐖𝐈𝐍 𝐕𝐈𝐏 𝐏𝐑𝐄𝐃𝐈𝐂𝐓𝐈𝐎𝐍 👑\n\n🎉 Welcome to the most trusted prediction platform! 🎉\n\n ✅ Join our official channel to stay updated.\n\n💡 After joining, click "I have Joined" to start using the bot!\n\n⚡️ Let's predict and win together!
    """
    
    image_url = "https://i.imghippo.com/files/XH1991cVA.jpg"
    keyboard = InlineKeyboardMarkup()
    join_button = InlineKeyboardButton("👉 𝙅𝙊𝙄𝙉 𝘾𝙃𝘼𝙉𝙉𝙀𝙇 👉", url=f"https://t.me/{CHANNEL_USERNAME}")
    joined_button = InlineKeyboardButton("✅ 𝙄 𝙃𝘼𝙑𝙀 𝙅𝙊𝙄𝙉𝙀𝘿 🙈", callback_data="check_joined")
    keyboard.add(join_button)
    keyboard.add(joined_button)
    
    bot.send_photo(chat_id, photo=image_url, caption=start_message, parse_mode="Markdown", reply_markup=keyboard)

# Callbacks for checking if user joined channel
def check_joined(bot, call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    try:
        member_status = bot.get_chat_member({CHANNEL_ID}, user_id).status
        if member_status in ['member', 'administrator', 'creator']:
            success_message = "🎉 **Thank you for joining!** 🎉\nNow you can access all premium features."
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("👉 𝙅𝙊𝙄𝙉 𝘾𝙃𝘼𝙉𝙉𝙀𝙇 👉", url=f"https://t.me/{CHANNEL_USERNAME}"), InlineKeyboardButton("💸 𝙁𝙍𝙀𝙀 𝙍𝙀𝘾𝙃𝘼𝙍𝙂𝙀 💸", callback_data="buy_apk")],
                [InlineKeyboardButton("✅ 𝙄 𝙃𝘼𝙑𝙀 𝙅𝙊𝙄𝙉𝙀𝘿 🙈", callback_data="check_joined")]
            ])
            bot.send_message(chat_id, success_message, parse_mode="Markdown", reply_markup=keyboard)
        else:
            bot.send_message(chat_id, "🚫 You haven't joined the channel yet. Please join first!")
    except Exception as e:
        bot.send_message(chat_id, f"❌ Error: {str(e)}\nMake sure the channel is public and the bot is an admin.")


def buy_apk(bot, call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    # Add invite and referral info
    user = users_collection.find_one({"user_id": user_id})
    points = user.get("points", 0)
    invite_message = f"""
📢 **Refer & Earn:**
Share your referral link to invite friends and earn points!

💡 **Your Refer Link**: `https://t.me/{BOT_USERNAME}?start={user_id}`

⭐ **You have {points} points.**
"""

    # Send invite and referral info with buttons
    keyboard = InlineKeyboardMarkup()
    invite_button = InlineKeyboardButton("👥 𝙄𝙉𝙑𝙄𝙏𝙀 𝙐𝙎𝙀𝙍𝙎 👥", callback_data="invite_user")
    paid_apk_button = InlineKeyboardButton("💸 𝙁𝙍𝙀𝙀 𝙍𝙀𝘾𝙃𝘼𝙍𝙂𝙀 💸", callback_data="buy_paid_apk")
    keyboard.add(invite_button)
    keyboard.add(paid_apk_button)

    bot.send_message(chat_id, invite_message, parse_mode="Markdown", reply_markup=keyboard)

def invite_user(bot, call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    # Add invite and referral info
    user = users_collection.find_one({"user_id": user_id})
    points = user.get("points", 0)
    invite_message = f"""
📢 **Refer & Earn:**
Share your referral link to invite friends and earn points

🔗 *Your Invite Link:* : "https://t.me/{BOT_USERNAME}?start={user_id}"

🔄 Forward this message to your friends & earn coins 💰
"""

    # Inline button to open forward option
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📤 Forward This Message", switch_inline_query=invite_message))

    # Message send karna jo user easily forward kar sake
    bot.send_message(chat_id, invite_message, parse_mode="MarkdownV2", reply_markup=markup)

def buy_paid_apk(bot, call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    # Fetch user data from MongoDB
    user = users_collection.find_one({"user_id": user_id})
    
    # Check if user exists and has points
    if user:
        points = user.get("points", 0)
        
        if points >= 1:
            # Enough points to buy APK
            bot.send_message(chat_id, "✅ Congratulations! You have enough points to buy the APK.\nContact @YourSupport for the APK.")
            
            # Deduct 1 point from the user's balance
            users_collection.update_one({"user_id": user_id}, {"$inc": {"points": -10}})

        else:
            # Not enough points
            bot.send_message(chat_id, f"❌ You need at least 10 point to buy the APK.\nCurrent Points: {points}\nRefer friends to earn points!")
            
            # Send message to others to collect points
            bot.send_message(chat_id, "💰 Collect more points by referring friends!")
    else:
        bot.send_message(chat_id, "❌ User not found in the database!")


# Function to Broadcast Text or Media
def broadcast(message):
    sender_id = message.from_user.id
    if sender_id != ADMIN_ID:
        bot.send_message(sender_id, "❌ You are not authorized to use this command!")
        return

    sent_count = 0
    users = users_collection.find({}, {"user_id": 1})

    # 🔹 **Media Broadcast (Reply to Media)**
    if message.reply_to_message:
        media_message = message.reply_to_message
        for user in users:
            try:
                if media_message.photo:
                    file_id = media_message.photo[-1].file_id
                    bot.send_photo(user["user_id"], file_id, caption=media_message.caption or "")
                elif media_message.video:
                    file_id = media_message.video.file_id
                    bot.send_video(user["user_id"], file_id, caption=media_message.caption or "")
                elif media_message.audio:
                    file_id = media_message.audio.file_id
                    bot.send_audio(user["user_id"], file_id, caption=media_message.caption or "")
                elif media_message.document:
                    file_id = media_message.document.file_id
                    bot.send_document(user["user_id"], file_id, caption=media_message.caption or "")
                sent_count += 1
            except:
                pass  # Agar user ne bot block kiya ho toh ignore karega

        bot.send_message(sender_id, f"✅ Media broadcasted to {sent_count} users!")

    # 🔹 **Text Broadcast**
    else:
        text = message.text.split(" ", 1)
        if len(text) < 2:
            bot.send_message(sender_id, "⚠️ Please provide a message to broadcast.\nExample: `/broadcast Hello everyone!`")
            return

        broadcast_text = text[1]
        for user in users:
            try:
                bot.send_message(user["user_id"], broadcast_text, parse_mode="Markdown")
                sent_count += 1
            except:
                pass  # Agar user ne bot block kiya ho toh ignore karega

        bot.send_message(sender_id, f"✅ Broadcast sent to {sent_count} users!")
