import paho.mqtt.client as mqtt
import json
from config import *

class MqttBot:

    # Khởi tạo MqttBot - Initialize MqttBot
    def __init__(self) -> None:
        self.mqtt = mqtt.Client()
        self.mqtt.connect(MQTT_BROKER, int(MQTT_PORT), 60)
        # self.username_pw_set(config.MQTT_USERNAME, config.MQTT_PASSWORD)
        self.mqtt.on_connect = self.on_connect
        self.mqtt.on_message = self.on_message

    # Hàm kiểm tra connect - Check connection
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to broker")
            self.mqtt.subscribe(ESP_TOPIC,2)
        else:
            print(f"Connected with result code {rc}")
    
    # Hàm xử lý khi nhận được message - Handle the message received
    def on_message(self,client,userdata,msg)-> None:
        global RELAY_STATUS
        try:
            if hasattr(msg, 'payload'):
                new_status = json.loads(msg.payload)
                RELAY_STATUS.update(new_status)
                print(str(RELAY_STATUS) + " from " + msg.topic)
            else:
                print("msg does not have payload attribute")
        except json.JSONDecodeError as e:
        # Nếu không thể chuyển đổi, gán giá trị payload - If can't convert, assign payload value
            RELAY_STATUS = msg.payload.decode('utf-8') if isinstance(msg.payload, bytes) else msg.payload

    
    # Hàm publish message - Publish message
    def publish(self, topic, message) -> None:
        try:
            msg = json.dumps(message)
            self.mqtt.publish(topic, msg, retain=True)
        except Exception as e:
            print(f"Error: {e}")
            self.publish(topic, message,retain=True)
    
    # Hàm chạy mqtt - Run mqtt
    def run(self) -> None:
        self.mqtt.loop_start()
