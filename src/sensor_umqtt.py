from umqtt.simple import MQTTClient

broker = "192.168.178.47"
port = 1883


def settimeout(duration):
    pass


client = MQTTClient("joe", broker, keepalive=60)
client.settimeout = settimeout
client.connect()

client.publish("sensor", str("1").encode())