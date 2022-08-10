import paho.mqtt.client as mqtt

client =mqtt.Client("client_name")
client.connect("dev-mint-pi")
client.publish("mqtt/pimylifeup","OFF")