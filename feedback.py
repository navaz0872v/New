from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime

# 🔐 Replace with your real bot token
BOT_TOKEN = '7836216459:AAEFRCJFTMre48e52PMQTOqvPedPEzAD_G4'

# 📨 Replace with your channel ID or username (make sure bot is admin there)
CHANNEL_ID = '-1002325438025'  # e.g. '@feedbackme09' or chat ID like -1002325438025

# 🔹 /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to the Feedback Bot!\n\n"
        "Use /feedback <your message> to share your thoughts.\n"
        "Use /help to view all available commands."
    )

# 🔹 /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🛠 *Available Commands:*\n\n"
        "/start - Welcome message\n"
        "/feedback <message> - Send feedback to the team\n"
        "/help - Show this help message\n\n"
        "📎 You can also send media (images, videos, files), and it will be forwarded to the admin channel."
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

# 🔹 /feedback <text>
async def handle_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "❗ Please provide feedback like this:\n\n`/feedback Your message here`",
            parse_mode='Markdown'
        )
        return

    feedback_text = ' '.join(context.args)
    sender = update.effective_user
    sender_name = sender.full_name
    username = f"@{sender.username}" if sender.username else "No username"
    time_sent = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = (
        f"📩 *New Feedback Received!*\n"
        f"👤 *From:* {sender_name} ({username})\n"
        f"🕒 *Time:* `{time_sent}`\n\n"
        f"💬 *Feedback:*\n{feedback_text}"
    )

    await context.bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='Markdown')
    await update.message.reply_text("✅ Your feedback has been sent. Thank you!")

# 🔹 Handle media (photo, video, file)
async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender = update.effective_user
    sender_name = sender.full_name
    username = f"@{sender.username}" if sender.username else "No username"
    time_sent = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    caption = (
        f"📩 *New Media Feedback!*\n"
        f"👤 *From:* {sender_name} ({username})\n"
        f"🕒 *Time:* `{time_sent}`\n\n"
        f"🖼️ Media attached."
    )

    if update.message.photo:
        await context.bot.send_photo(chat_id=CHANNEL_ID, photo=update.message.photo[-1].file_id, caption=caption, parse_mode='Markdown')
    elif update.message.document:
        await context.bot.send_document(chat_id=CHANNEL_ID, document=update.message.document.file_id, caption=caption, parse_mode='Markdown')
    elif update.message.video:
        await context.bot.send_video(chat_id=CHANNEL_ID, video=update.message.video.file_id, caption=caption, parse_mode='Markdown')

    await update.message.reply_text("✅ Your media feedback has been forwarded. Thanks!")

# 🔧 Main function
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("feedback", handle_feedback))
    app.add_handler(MessageHandler(filters.PHOTO | filters.DOCUMENT | filters.VIDEO, handle_media))

    print("🤖 Feedback Bot is running...")
    app.run_polling()

# 🏁 Run
if __name__ == '__main__':
    main()