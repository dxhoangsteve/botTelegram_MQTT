from config import *
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, CallbackContext
from pytz import timezone


# Hàm xử lý lệnh /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    # Trả lời khi người dùng gửi lệnh /start - Reply to the user when they send the /start command
    await update.message.reply_text("Hello, I'm hear")

# Kiểm tra trạng thái của relay - Check the status of the relay

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE)-> None:
    await update.message.reply_text(f"Status:  {RELAY_STATUS}")

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton("ON", callback_data='ON'),
            InlineKeyboardButton("OFF", callback_data='OFF'),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('Chọn trạng thái relay: ', reply_markup=reply_markup)

# Hàm xử lý khi người dùng nhấn vào một nút
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    # Trả lời truy vấn để đóng trạng thái "loading"
    await query.answer()

    # Xử lý dữ liệu từ nút được nhấn
    if query.data == 'ON':
        RELAY_STATUS = 'ON'
        await query.edit_message_text(text="/status để kiểm tra trạng thái relay", reply_markup=None)
    elif query.data == 'OFF':
        RELAY_STATUS = 'OFF'
        await query.edit_message_text(text="/status để kiểm tra trạng thái relay", reply_markup=None)
    
    try:
        await query.edit_message_reply_markup(reply_markup=None)
    except Exception as e:
        print(f"Error: {e}")  # In lỗi nếu có

# Hàm xử lý lệnh /help - Handle the /help command
async def help_command(update: Update, context: CallbackContext) -> None:
    help_text = (
        "/start - Bắt đầu với bot\n"
        "/help - Hiển thị tất cả các lệnh\n"
        "/status - Hiển thị giá trị của biến status\n"
        "/setting - Hiển thị hộp thoại để đổi giá trị biến status"
    )
    await update.message.reply_text(help_text)

def main() -> None:

    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.job_queue.scheduler.configure(timezone=timezone('UTC'))

    # Đăng ký các handler - Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("settings", settings))

    # Khởi động bot
    application.run_polling()

if __name__ == '__main__':
    main()
