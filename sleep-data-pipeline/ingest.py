import os, json, time
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion

BROKER_HOST = os.getenv("BROKER_HOST", "192.168.1.37")
BROKER_PORT = int(os.getenv("BROKER_PORT", "1883"))
TOPIC       = os.getenv("TOPIC", "sensors/+/data")

def on_connect(client, userdata, flags, rc, properties=None):
    print(f"[Connected] rc={rc}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload)
        print(f"[{msg.topic}] => {payload}")
    except json.JSONDecodeError:
        print(f"Invalid JSON: {msg.payload}")

def main():
    client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message

    while True:
        try:
            print(f"Connecting to {BROKER_HOST}:{BROKER_PORT}…")
            client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
            break
        except Exception as e:
            print(f"Connection error: {e}. Retry in 5s")
            time.sleep(5)

    client.loop_forever()

if __name__ == "__main__":
    main()
