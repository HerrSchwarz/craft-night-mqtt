import network
import time
import upip

ssid="Villa Muk"
password="sY6vA607Ftn3V4Gc5BvA"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid,password)

while not wlan.isconnected() and wlan.status() >= 0:
	print("Waiting to connect:")
	time.sleep(1)

upip.install('umqtt.simple')