#CRAFT-NIGHT-MQTT

#How To Setup Mosquitto Broker on RPi4B and Client on Linux and RPi Pico
Based on this [Tutorial](https://pimylifeup.com/raspberry-pi-mosquitto-mqtt-server/)

##Install the Broker and Client on the RPi4B
First update your system:

`sudo apt update`
`sudo apt upgrade -y`

Then install the Broker and and client

`sudo apt install mosquitto mosquitto-clients`

Now check that the service is running on your Pi

`sudo systemctl status mosquitto.service`
There should be a green "(is running)" in the console output

This Broker only allows communication on the system, remote devices like other PCs and Microcontrollers will not be able to interact with the broker. To fix this, the config file has to be changed.

Open the config file using your preferred editor (nano in this case)

`sudo nano /etc/mosquitto/mosquitto.conf`

and add the following two lines at at the end of the file

`listener 1883`
`allow_anonymous true`

This tells the Broker that Port 1883 is used for communication with network devices and to allow devices without a username and password to write to allow access to the topics.

Now save and close the file.
In nano: CTRL+o -> ENTER -> CTRL+x

For the changes to apply, the Broker has to be restarted
`sudo systemctl stop mosquitto.service`
`sudo systemctl restart mosquitto.service`

Check that the Broker is running
`sudo systemctl status mosquitto.service`

###Subscribing and Publishing to a Topic
Clients comunicate with the Broker through Topics. They can either Publish messages to a Topic or Subscribe to a Topic to receive messages that other clients Published to it.

On the RPi open a new console and type in the following command to Subscribe to a Topic

`mosquitto_sub -h localhost -t "YOUR_TOPIC"`
Please keep this console open for the rest of this whole Tutorial.

`"YOUR_TOPIC"` may be changed to something like `"my_test"`
Now this console will continuously wait for anything to be Published to it and print it to the console

To do this, open another console and type the following command to Publish to a Topic

`mosquitto_pub -h localhost -t "YOUR_TOPIC" -m "YOUR_MESSAGE"`

Exchange `"YOUR_TOPIC"` for the name you chose and substitute `"YOUR_MESSAGE"` for whatever message you want to Publish.

Once youexectue this command, the message pops up in the console that Subscribed to the Topic.

##Publishing from External Devices
Publishing from external devices was made possible by adding the two lines above to the `mosquitto.conf file`. To Publish something to a Topic the Broker and Client have to be in the same network.

###Python(Tested on Linux PC)
For Publishing with Python the paho MQTT package is used. Install it using the following command
`pip install paho-mqtt`

Afterwards the `mqtt_linux.py` file included in this repo can be run to Publish a message to your Broker.
Please configure the values of `"BROKER_IP"` (IP-Adress of the RPi4), `"YOUR_TOPIC"` and `"YOUR_MESSAGE"` according to your setup. 

After executing this code your message should pop up in the Console on your RPi4 which Subscribed to the Topic.

###Micropython(Tested On RPi Pico W with Linux PC)

If you do not already have Micropython installed on your RPi Pico W, the current Micropython Version can be downloaded [here](https://micropython.org/download/rp2-pico-w/). Just download the latest version, connect your RPi Pico to the PC using a Micro-USB cable and it should pop up as an external drive.
Copy the downloaded file directly into the drive and wait for a couple of seconds. The drive should now not be visible anymore, or at least the files previously visible are not there anymore.
This means everything worked

###Installing ampy
ampy, a package created by adafruit, allows writing files and executing Micropython code on a microcontroller from the command line. Execute the following code to install it.
`pip install adafruit-ampy`

Also to find the port to which the Pico is connected you need the serial package, if it is not yet installed, use the following command.

`pip install serial`

###Installing MQTT package for Micropython
The MQTT package is, as of now, not part of the standard distribution libraries and needs to be installed manually.
To do this the Pico must connect to the Wifi and download the package. The `pico_pi_umqtt_install.py` file included in this repository handles this. Again, please change the `ssid` and `password` values to your network's specifications and then run the script.

Now to figure out which port the Pico is connected to, run the `find_comports.py` included in this repository. It will print a list of all connected devices' comports.

Once you got your port which on Linux looks something like `/dev/ttyACM0` execute the following command after adapting the values.

`ampy --port "YOUR_PICO_PI_PORT" run ../pico_pi_umqtt_install.py`
e.g.
`ampy --port '/dev/ttyACM0' run pico_pi_umqtt_install.py`

This will run the script on your Pico without actually writing it onto the microcontroller, because it only has to be executed once. This is due to how the `run` argument is set up.

If the script executes correctly, the console should show, that the umqtt package was installed on the Pico.

###Publishing a Topic to the Broker
Now everything is se up. The `boot.py` contains all the code necessary to Publish to a Topic. You need to change the following values to your specification, all of which have already been set at a pervious point in this tutorial:
`ssid` -> your networks' SSID (line 7)
`password` -> your networks' password (line 8)
`mqtt_server` -> set to your RPi4's IP Adress (line 19)
`topic_pub` -> set to the Topic you want to Publish to (line 21)
`YOUR_MESSAGE` -> change the String to the message you want to send (line 48)

The rest can be left as is. Now, the reason this python file is named `boot.py` is beacuse the file by this name on the Pico is automatically run on boot. Now write this file onto the Pico using `ampy` again. This time instead of `run` you can also use the argument `put`. This will actually override the previous `boot.py` file on the Pico.
For the sake of this tutorial the `run` option is recommended.

So use either
`ampy --port "YOUR_PICO_PI_PORT" put ../boot.py`
or
`ampy --port "YOUR_PICO_PI_PORT" run ../boot.py`
and change the port and filepath accordingly again.

If you used the `put` option you may have to disconnect and reconnect your Pico since it needs to reboot for the script to run.

After connecting to the network the message is Published to the Topic and should show up in the console on the RPi4 that Subscribed to the Topic.


##Aaaaaand DONE :)
