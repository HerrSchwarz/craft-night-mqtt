import machine
import network
import utime
from umqtt.simple import MQTTClient

ssid=""
password=""
mqtt_server = ''

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid,password)

while not wlan.isconnected() and wlan.status() >= 0:
	print("Waiting to connect:")
	utime.sleep(1)


client_id = 'PicoW'
topic_pub = 'HEAD_TOPIC/FROM_MC'
topic_sub = 'HEAD_TOPIC/TO_MC'

last_message = 0
message_interval = 5
counter = 0
BLINKING_FREQUENCY_HZ = 1
PUBLISHING_INTERVAL_S = 5
led = machine.Pin(2, machine.Pin.OUT)



def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, keepalive=60)
    client.set_callback(my_callback)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

def reconnect():
    print('Failed to connected to MQTT Broker. Reconnecting...')
    utime.sleep(5)
    machine.reset()

def my_callback(topic, msg):
    #PUBLISHING EXAMPLE FOR SERVER: mosquitto_pub -h localhost -t "HEAD_TOPIC/TO_MC" -m "2:6"
    #Format:     BLINKING_FREQUENCY_HZ:PUBLISHING_INTERVAL_S
    global BLINKING_FREQUENCY_HZ, PUBLISHING_INTERVAL_S
    print((topic, msg))
    if topic.decode("utf-8") == topic_sub:
        try:
            msg = msg.decode("utf-8")
            values = msg.split(":")
            BLINKING_FREQUENCY_HZ=int(values[0])
            PUBLISHING_INTERVAL_S=int(values[1])
        except Exception as e:
            print(e)


#connecting_to_client
try:
    client = mqtt_connect()
except OSError as e:
    reconnect()

client.subscribe(topic_sub) 
last_published_time=utime.ticks_ms()
counter = 0

while True:
    client.check_msg()
    if utime.ticks_diff(utime.ticks_ms(),last_published_time)/1000 > PUBLISHING_INTERVAL_S:
        counter += 1
        client.publish(topic_pub, msg=f'{counter}. Message')
        print("published")
        last_published_time=utime.ticks_ms()
    else:
        print(utime.ticks_diff(utime.ticks_ms(),last_published_time)/1000)

    led.on()
    utime.sleep(1/(BLINKING_FREQUENCY_HZ*2))
    led.off()
    utime.sleep(1/(BLINKING_FREQUENCY_HZ*2))
