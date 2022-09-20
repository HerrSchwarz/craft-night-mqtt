import paho.mqtt.client as mqtt
import time

broker = 'localhost'
port = 1883
topic = "sensor"
client_id = 'server'


class Server:
    # The callback for when the client receives a CONNACK response from the server.
    @staticmethod
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(topic)

    # The callback for when a PUBLISH message is received from the server.
    @staticmethod
    def on_message(client, userdata, msg):
        message = msg.payload.decode('utf-8')
        print("message received:")
        print(msg.topic+" "+str(message))
        if int(message) > 20:
            client.publish("rate", payload=1)
        else:
            client.publish("rate", payload=5)

    def __init__(self):
        client = mqtt.Client(client_id, True, None, mqtt.MQTTv31)
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(broker, port, 60)

        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        client.loop_forever()

    
Server()
