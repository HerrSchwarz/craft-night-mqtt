import paho.mqtt.client as mqtt

client =mqtt.Client("client_name")
client.connect("BROKER_IP")
client.publish("YOUR_TOPIC","YOUR_MESSAGE")