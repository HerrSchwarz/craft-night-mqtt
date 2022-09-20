import paho.mqtt.client as mqtt

broker = "localhost"
port = 1883
client = mqtt.Client("publisher")
client.connect(broker, port)

client.publish("rate", payload=10)
