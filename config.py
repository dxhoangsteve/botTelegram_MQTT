from dotenv import load_dotenv
import os

load_dotenv()

# MQTT setting
MQTT_BROKER = os.getenv('MQTT_BROKER')
MQTT_USER = os.getenv('MQTT_USER')
MQTT_PASS = os.getenv('MQTT_PASS')
MQTT_PORT = os.getenv('MQTT_PORT')

BOT_TOPIC= os.getenv('BOT_PUB')
ESP_TOPIC= os.getenv('ESP_PUB')

# Telegram bot setting
TELEGRAM_TOKEN= os.getenv('TELEGRAM_TOKEN')
ALLOWED_IDS = os.getenv('ALLOWED_IDS').split(',')

RELAY_STATUS = {
    "relay": "OFF",
    "led": "OFF"
}