import os
import json
import time
import paho.mqtt.client as mqtt
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

BROKER_HOST = os.getenv("BROKER_HOST", "mosquitto")
BROKER_PORT = int(os.getenv("BROKER_PORT", 1883))
TOPIC       = os.getenv("TOPIC", "sensors/+/data")
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092")
KAFKA_TOPIC     = os.getenv("KAFKA_TOPIC", "raw-sensor-data")

def create_producer():
    while True:
        try:
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BOOTSTRAP,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            print(f"[INGEST] Connected to Kafka @ {KAFKA_BOOTSTRAP}")
            return producer
        except NoBrokersAvailable:
            print(f"[INGEST] Kafka not available at {KAFKA_BOOTSTRAP}, retrying in 5s…")
            time.sleep(5)

# Önce Kafka’ya bağlanmayı deneyelim (retry)
producer = create_producer()

def on_connect(client, userdata, flags, rc):
    print(f"[INGEST] Connected to MQTT (rc={rc}), subscribing to {TOPIC}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        print(f"[INGEST] Invalid JSON: {payload}")
        return

    print(f"[INGEST] {msg.topic} → {data}")
    producer.send(KAFKA_TOPIC, data)
    producer.flush()

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER_HOST, BROKER_PORT, 60)
    client.loop_forever()

if __name__ == "__main__":
    main()

