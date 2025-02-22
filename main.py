from telegramBot import TelegramBot
from mqtt import MqttBot
from config import *
def main() -> None:
    Mqtt = MqttBot()
    Mqtt.run()
    bot = TelegramBot(Mqtt)
    bot.run()
    
if __name__ == '__main__':
    main()
