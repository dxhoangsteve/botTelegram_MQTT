# đây là file dùng để cấu hình bot telegram - this file used config bot telegeram

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ContextTypes, CallbackQueryHandler, Application

from config import TELEGRAM_TOKEN, ALLOWED_IDS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    # kiểm tra id người dùng có trong danh sách cho phép không - check id user in list allowed or not

    if update.effective_user.id in ALLOWED_IDS:
        await update.message.reply_text("Hello! I'm a bot!")
    else:
        await update.message.reply_text("You are not allowed to use this bot.")

    # sau khi ấn start bot sẽ hiện ra menu - after press start bot will show menu

    await update.message.reply_text("🤖 Bot điều khiển Relay\n"
        "Sử dụng lệnh:\n"
        "/status - Xem trạng thái\n"
        "/setting - Thay đổi trạng thái")

# lệnh /status để xem trạng thái - command /status to see status
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ALLOWED_IDS:
        return
    status_text = f"🔌 Trạng thái hiện tại: {RELAY_STATUS}"
    keyboard = [InlineKeyboardButton("⚙️ Cài đặt", callback_data='setting')]
    reply_markup = InlineKeyboardMarkup([keyboard])

    # trả lời tin nhắn với trạng thái và nút cài đặt - reply message with status and setting button
    await update.message.reply_text(
        text=status_text,
        reply_markup=reply_markup
    )

# xử lý /setting - handle /setting
async def setting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ALLOWED_IDS:
        return
    
    keyboard = [
        [
            InlineKeyboardButton("🟢 BẬT", callback_data="ON"),
            InlineKeyboardButton("🔴 TẮT", callback_data="OFF")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        text="Chọn trạng thái Relay:",
        reply_markup=reply_markup
    )



def setup_bot():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("setting", setting))
    
    return application