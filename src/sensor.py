import random
import time
import paho.mqtt.client as mqtt
import threading

broker = "192.168.178.47"
port = 1883


class Sensor:

    interval = 5

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("rate")
        self.publish()

    def publish(self):
        print("sending new message")
        self.client.publish("sensor", random.randint(10, 30))
        print(f"Sending next value in {self.interval} seconds")
        timer = threading.Timer(self.interval, self.publish)
        timer.start()

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, mqtt, userdata, msg):
        message = msg.payload.decode('utf-8')
        print(f"new interval: {message}")
        self.interval = int(message)

    def __init__(self):
        self.client = mqtt.Client("sensor", True, None, mqtt.MQTTv31)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(broker, port, 60)
        self.client.loop_forever()


sensor = Sensor()
