import json
from mqtt import MqttBot
from config import *
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, CallbackContext
from pytz import timezone

class TelegramBot:
    # Khởi tạo TelegramBot - Initialize TelegramBot
    def __init__(self, mqtt: MqttBot) -> None:
        self.mqtt = mqtt
        self.application = Application.builder().token(TELEGRAM_TOKEN).build()
        self.application.job_queue.scheduler.configure(timezone=timezone('UTC'))

    # Đăng ký các handler - Register handlers
    def regist_handler(self) -> None:
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CallbackQueryHandler(self.button))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("status", self.status))
        self.application.add_handler(CommandHandler("settings", self.settings))

    # Hàm xử lý lệnh /start
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Hello, I'm here")

    # Kiểm tra trạng thái của relay - Check the status of the relay
    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(f"Status: {RELAY_STATUS['relay']}")

    # Hiển thị menu cài đặt relay
    async def settings(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        keyboard = [
            [
                InlineKeyboardButton("ON", callback_data='ON'),
                InlineKeyboardButton("OFF", callback_data='OFF'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('Chọn trạng thái relay:', reply_markup=reply_markup)

    # Xử lý khi người dùng nhấn vào một nút
    async def button(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()

        if query.data == 'ON':
            RELAY_STATUS["relay"] = "ON"
            text = "/status để kiểm ra trạng thái relay"
        elif query.data == 'OFF':
            RELAY_STATUS["relay"] = "OFF"
            text = "/status để kiểm tra trạng thái relay"

        try:
            await query.edit_message_text(text=text, reply_markup=None)
            print(json.dumps(RELAY_STATUS))
            self.mqtt.publish(BOT_TOPIC, RELAY_STATUS)
        except Exception as e:
            print(f"Error: {e}")  

    # Hàm xử lý lệnh /help - Handle the /help command
    async def help_command(self, update: Update, context: CallbackContext) -> None:
        help_text = (
            "/start - Bắt đầu với bot\n"
            "/help - Hiển thị tất cả các lệnh\n"
            "/status - Hiển thị giá trị của biến status\n"
            "/settings - Hiển thị hộp thoại để đổi giá trị biến status"
        )
        await update.message.reply_text(help_text)

    # Hàm chạy bot - Run the bot
    def run(self) -> None:
        self.regist_handler()  # Đăng ký các handler
        self.application.run_polling()  # Chạy bot