from telegramBot import TelegramBot
from mqtt import MqttBot
from config import *
def main() -> None:
    # bot = TelegramBot()
    # bot.run()
    Mqtt = MqttBot()
    Mqtt.run()
    try:
        while True:
            # Nhập tin nhắn từ người dùng trong terminal
            message = input("Nhập tin nhắn (dạng json nếu không sẽ gửi dạng text) để publish (hoặc 'exit' để thoát): ")
            if message.lower() == 'exit':
                break
            # Publish tin nhắn lên topic
            Mqtt.mqtt.publish(STATUS_TOPIC, message)
            print(f"Tin nhắn '{message}' đã được publish tới topic '{STATUS_TOPIC}'")

    except KeyboardInterrupt:
        print("Ngắt kết nối...")

    finally:
        # Dừng client và ngắt kết nối
        Mqtt.mqtt.loop_stop()
        Mqtt.mqtt.disconnect()

if __name__ == '__main__':
    main()
