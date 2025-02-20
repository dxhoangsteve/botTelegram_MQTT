from config import TELEGRAM_TOKEN
from telegram import Update
from telegram.ext import CallbackContext, Updater, CommandHandler


def start(update: Update, context: CallbackContext):
    """Gửi tin nhắn khi lệnh /start được phát ra."""
    update.message.reply_text('Chào mừng bạn đến với bot của tôi!')

def help_command(update: Update, context: CallbackContext):
    """Gửi tin nhắn khi lệnh /help được phát ra."""
    update.message.reply_text('Bạn có thể sử dụng các lệnh sau: /start, /help')
