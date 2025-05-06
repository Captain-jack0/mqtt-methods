import os, json, time 
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion

BROKER_HOST = os.getenv("BROKER_HOST", "192.168.1.55")    #MQTT adresi
BROKER_PORT = int(os.getenv("BROKER_PORT", "1883"))
TOPIC       = "sensors/+/data"  # tüm sensör topic’leri için wildcard

def on_connect(client, userdata, flags, rc):
    print(f"Bağlandı, sonuç kodu: {rc}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload)
        print(f"[{msg.topic}] => {payload}")
    except json.JSONDecodeError:
        print(f"Geçersiz JSON: {msg.payload}")

def main():
    client = mqtt.Client()
    client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2)    
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    client.loop_forever()

if __name__ == "__main__":
    main()

