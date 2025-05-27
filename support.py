
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

SUPPORT_BOT_TOKEN = "7772419235:AAFhFo4h9t5NVaVlNgDe_ifK8zEnGwRPOpQ"
ADMIN_CHAT_ID = "6711531095" # Your Telegram ID or admin group chat ID

bot = telebot.TeleBot(SUPPORT_BOT_TOKEN)

# /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📤 Send Screenshot", callback_data="send_ss"),
        InlineKeyboardButton("⬅️ Back To FxTradify Bot", url="https://t.me/FxTradifyBot")
    )
    
    bot.send_message(message.chat.id, 
        """📌 Welcome to FxTradify Premium Signals!

This isn’t your average signal group. We drop real, high-converting trades — not spammy gold BS.

📩 Press "Send Screenshot" and upload your broker screenshot.

💰 Once verified, you'll receive lifetime VIP access.
""", reply_markup=markup
    )

# Handle button press
@bot.callback_query_handler(func=lambda call: call.data == "send_ss")
def ask_screenshot(call):
    bot.send_message(call.message.chat.id, "📸 Please send your payment screenshot now...")

# Handle screenshot upload
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # Forward photo to admin
    bot.forward_message(ADMIN_CHAT_ID, message.chat.id, message.message_id)

    # Notify admin with user info + button
    user = message.from_user
    username = f"@{user.username}" if user.username else "No Username"
    full_name = f"{user.first_name} {user.last_name or ''}".strip()

    view_user_button = InlineKeyboardMarkup()
    view_user_button.add(InlineKeyboardButton("💬 Message User", url=f"https://t.me/{user.username}" if user.username else "https://t.me"))

    bot.send_message(
        ADMIN_CHAT_ID,
        f"📥 New Screenshot from:\n👤 Name: {full_name}\n🔗 Username: {username}",
        reply_markup=view_user_button
    )

    # Acknowledge to user
    bot.send_message(message.chat.id, "✅ Screenshot received. Our team will review and get back to you shortly.")

print("✅ Support Bot is running...")
bot.infinity_polling()
