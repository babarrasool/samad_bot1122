import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, filters

# 🔑 Your Credentials & Links
TOKEN = "7786155773:AAG5d5FYhqNXsdNXqZ21umJyhkKXxq_J6-g"
WHATSAPP_LINK = "https://whatsapp.com/channel/0029VbAknvc9sBIFbzgeCT2V"
YOUTUBE_LINK = "https://youtube.com/@samadcolortradingvip?si=1copsO7FRkOpnPYh"

# 🎲 Prediction Logic
def get_signal(time_frame, period):
    signal_color = random.choice(["GREEN", "RED"])
    signal_size = random.choice(["BIG", "SMALL"])
    win_rate = random.randint(75, 95)
    
    return f"""🎯 PREMIUM SIGNAL  
━━━━━━━━━━━━━━  
📊 SIGNAL: {signal_color} / {signal_size}  
⏳ TIME: {time_frame}  
🔢 PERIOD: {period}  
📈 WIN RATE: {win_rate}%"""

# 🚀 Enhanced Start Command with Dual Channel
async def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    keyboard = [
        [InlineKeyboardButton("📱 Join WhatsApp", url=WHATSAPP_LINK)],
        [InlineKeyboardButton("🎥 Subscribe YouTube", url=YOUTUBE_LINK)],
        [InlineKeyboardButton("✅ Verify & Continue", callback_data="check_join")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"🌟 Welcome {user.first_name}!\n\n"
        "To access premium signals, please:\n"
        "1. Join our WhatsApp channel\n"
        "2. Subscribe YouTube channel",
        reply_markup=reply_markup
    )

# 🔄 Updated Verification Message
async def check_join(update: Update, context: CallbackContext):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("⚡ 30 Seconds", callback_data="wingo_30s")],
        [InlineKeyboardButton("⏳ 1 Minute", callback_data="wingo_1m")],
        [InlineKeyboardButton("⏲️ 3 Minutes", callback_data="wingo_3m")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(
        "✅ Access Granted!\n\n"
        "Choose your trading timeframe:",
        reply_markup=reply_markup
    )

# 🎮 Rest of the code remains the same
async def wingo(update: Update, context: CallbackContext):
    query = update.callback_query
    time_frame = ""
    
    if query.data == "wingo_30s":
        time_frame = "30 SEC"
    elif query.data == "wingo_1m":
        time_frame = "1 MIN"
    elif query.data == "wingo_3m":
        time_frame = "3 MIN"

    context.user_data["time_frame"] = time_frame

    await query.message.reply_text(
        f"""⏱ MODE SELECTED  
Time Frame: {time_frame}  
━━━━━━━━━━━━━━  
Enter last 3 digits of period:"""
    )

async def receive_period(update: Update, context: CallbackContext):
    period = update.message.text.strip()
    
    if not period.isdigit() or len(period) != 3:
        await update.message.reply_text("❌ Please enter exactly 3 digits.")
        return
    
    time_frame = context.user_data.get("time_frame", "Unknown")

    signal = get_signal(time_frame, period)

    keyboard = [
        [InlineKeyboardButton("🔄 New 30s Trade", callback_data="wingo_30s")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(signal, reply_markup=reply_markup)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))
    app.add_handler(CallbackQueryHandler(wingo, pattern="wingo_.*"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_period))

    print("🚀 Bot is fully operational!")
    app.run_polling()

if __name__ == "__main__":
    main()
