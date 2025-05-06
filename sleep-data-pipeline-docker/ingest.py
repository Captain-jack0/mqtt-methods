import os, json
import paho.mqtt.client as mqtt

BROKER_HOST = os.getenv("BROKER_HOST","mosquitto")
BROKER_PORT = int(os.getenv("BROKER_PORT", 1883))
TOPIC       = os.getenv("TOPIC", "sensors/+/data")

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
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    client.loop_forever()

if __name__ == "__main__":
    main()
