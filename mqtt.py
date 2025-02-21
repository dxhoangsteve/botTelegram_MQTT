import paho.mqtt.client as mqtt
import json
import config

class MqttBot:

    # Khởi tạo MqttBot - Initialize MqttBot
    def __init__(self) -> None:
        self.mqtt = mqtt.Client()
        self.mqtt.connect(config.MQTT_BROKER, int(config.MQTT_PORT), 60)
        # self.username_pw_set(config.MQTT_USERNAME, config.MQTT_PASSWORD)
        self.mqtt.on_connect = self.on_connect
        self.mqtt.on_message = self.on_message

    # Hàm kiểm tra connect - Check connection
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to broker")
            self.mqtt.subscribe(config.STATUS_TOPIC)
        else:
            print(f"Connected with result code {rc}")
    
    # Hàm xử lý khi nhận được message - Handle the message received
    def on_message(self,userdata,msg)-> None:
        try:
            message = json.loads(msg.payload)
            print(message+ " from "+msg.topic)
        except Exception as e:
            print(f"Error: {e}")
    
    # Hàm publish message - Publish message
    def publish(self, topic, message) -> None:
        try:
            msg = json.dumps(message)
            self.mqtt.publish(topic, msg)
        except Exception as e:
            print(f"Error: {e}")
            self.publish(topic, message)
    
    # Hàm chạy mqtt - Run mqtt
    def run(self) -> None:
        self.mqtt.loop_start()
