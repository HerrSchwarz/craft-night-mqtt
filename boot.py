import machine
import network
import time
from umqtt.simple import MQTTClient

print "trying to connect to Wifi"

ssid="Villa Muk"
password="sY6vA607Ftn3V4Gc5BvA"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid,password)

while not wlan.isconnected() and wlan.status() >= 0:
	print("Waiting to connect:")
	time.sleep(1)


mqtt_server = 'BROKER_IP'
client_id = 'PicoW'
topic_pub = 'YOUR_TOPIC'

last_message = 0
message_interval = 5
counter = 0



def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, keepalive=60)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

def reconnect():
    print('Failed to connected to MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()

while True:
    try:
        client = mqtt_connect()
    except OSError as e:
        reconnect()

    while True:
        try:
            client.publish(topic_pub, msg='YOUR_MESSAGE')
            print('published')
            time.sleep(3)
        except:
            reconnect()
            pass
        client.disconnect()
