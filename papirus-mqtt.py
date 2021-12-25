#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Subscribe to MQTT and print Topics to an epaper display
"""
from __future__ import print_function
from datetime import datetime, timedelta
from PIL import Image, ImageFont, ImageDraw
from papirus import Papirus
import os
import sys
import paho.mqtt.client as mqtt
__version__ = '0.2'
__author__ = 'Dominic Spatz'

# Check EPD_SIZE is defined
EPD_SIZE = 0.0
if os.path.exists('/etc/default/epd-fuse'):
    with open('/etc/default/epd-fuse') as infile:
        exec(infile.read())
if EPD_SIZE == 0.0:
    print("Please select your screen size by running 'papirus-config'.")
    sys.exit()

# Running as root only needed for older Raspbians without /dev/gpiomem
if not (os.path.exists('/dev/gpiomem') and os.access('/dev/gpiomem', os.R_OK | os.W_OK)):
    user = os.getuid()
    if user != 0:
        print("Please run script as root")
        sys.exit()

WHITE = 1
BLACK = 0

power = "0"
consumption = "0"
temperature = "0"
humidity = "0"
temperature2 = "0"
humidity2 = "0"
download = "0"
upload = "0"
power_prev = "0"
consumption_prev = "0"
temperature_prev = "0"
humidity_prev = "0"
temperature2_prev = "0"
humidity2_prev = "0"
download_prev = "0"
upload_prev = "0"
last_refresh = datetime.now()
client_id = "epaper"
mqtthost = "10.0.2.0"
port = 1883
keepalive = 60
debug = True

screen = Papirus(rotation=180)

print('panel = {p:s} {w:d} x {h:d}  version={v:s} COG={g:d} FILM={f:d}'.format(p=screen.panel, w=screen.width, h=screen.height, v=screen.version, g=screen.cog, f=screen.film))
screen.clear()


"""
Subscribing in on_connect: If we lose connection and reconnect then subscriptions will be renewed
"""


def on_connect(client, userdata, flags, rc):
    if(debug):
        print("Connected to mqtt host "+mqtthost+" with result code "+str(rc))
    mqttclient.subscribe([("epaper/power", 2), ("epaper/cons_d", 2), ("epaper/temp_indoor", 2), ("epaper/humi_indoor", 2), ("epaper/temp_outdoor", 2), ("epaper/humi_outdoor", 2), ("epaper/download", 2), ("epaper/upload", 2)])
    image = Image.new('1', screen.size, WHITE)
    draw = ImageDraw.Draw(image)

    font_path = "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"
    font_title = ImageFont.truetype(font_path, 17)
    font_values = ImageFont.truetype(font_path, 15)

    draw.text((0, 0), "Smarthome ", font=font_title, fill=0)
    draw.text((125, 0), (datetime.now().strftime("%H:%M")) + " Uhr", font=font_title, fill=0)
    draw.text((0, 20), "Connected to "+mqtthost+":"+str(port), font=font_values, fill=0)
    screen.display(image)
    update_screen()

"""
Store values from the mqtt topics in the variables
"""


def on_message(mqtt, obj, msg):
    global power, consumption, temperature, humidity, temperature2, humidity2, download, upload, power_prev, consumption_prev, temperature_prev, humidity_prev, temperature2_prev, humidity2_prev, download_prev, upload_prev

    if msg.topic == "epaper/power":
        power = str(int(float(msg.payload)))
    if msg.topic == "epaper/cons_d":
        consumption = str(round(float(msg.payload), 3)).replace('.', ',')
    if msg.topic == "epaper/temp_indoor":
        temperature = str(round(float(msg.payload), 1)).replace('.', ',')
    if msg.topic == "epaper/humi_indoor":
        humidity = str(round(float(msg.payload), 1)).replace('.', ',')
    if msg.topic == "epaper/temp_outdoor":
        temperature2 = str(round(float(msg.payload), 1)).replace('.', ',')
    if msg.topic == "epaper/humi_outdoor":
        humidity2 = str(round(float(msg.payload), 1)).replace('.', ',')
    if msg.topic == "epaper/download":
        download = str(round(float(msg.payload), 1)).replace('.', ',')
    if msg.topic == "epaper/upload":
        upload = str(round(float(msg.payload), 1)).replace('.', ',')
    if power != power_prev:
        power_prev = power
        display_data()
    if consumption != consumption_prev:
        consumption_prev = consumption
        display_data()
    if temperature != temperature_prev:
        temperature_prev = temperature
        display_data()
    if humidity != humidity_prev:
        humidity_prev = humidity
        display_data()
    if temperature2 != temperature2_prev:
        temperature2_prev = temperature2
        display_data()
    if humidity2 != humidity2_prev:
        humidity2_prev = humidity2
        display_data()
    if download != download_prev:
        download_prev = download
        display_data()
    if upload != upload_prev:
        upload_prev = upload
        display_data()


"""
Display data on the screen
"""


def display_data():
    global power
    global consumption
    global temperature
    global humidity
    global temperature2
    global humidity2
    global download
    global upload
    image = Image.new('1', screen.size, WHITE)
    draw = ImageDraw.Draw(image)

    font_path = "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"
    font_title = ImageFont.truetype(font_path, 17)
    font_values = ImageFont.truetype(font_path, 15)

    draw.text((0, 0), "Smarthome ", font=font_title, fill=0)
    draw.text((125, 0), (datetime.now().strftime("%H:%M")) + " Uhr", font=font_title, fill=0)
    draw.text((0, 20), "Strom", font=font_values, fill=0)
    draw.text((65, 20), power + " W ", font=font_values, fill=0)
    draw.text((125, 20), consumption + " kWh", font=font_values, fill=0)
    draw.text((0, 40), "Klima", font=font_values, fill=0)
    draw.text((65, 40), temperature + " \xb0C ", font=font_values, fill=0)
    draw.text((125, 40), humidity + " % RH", font=font_values, fill=0)
    draw.text((0, 60), "Wetter", font=font_values, fill=0)
    draw.text((65, 60), temperature2 + " \xb0C ", font=font_values, fill=0)
    draw.text((125, 60), humidity2 + " % RH", font=font_values, fill=0)
    draw.text((0, 80), "Internet", font=font_values, fill=0)
    draw.text((65, 80), download + " DL", font=font_values, fill=0)
    draw.text((125, 80), upload + " UL", font=font_values, fill=0)
    screen.display(image)
    update_screen()


def update_screen():
    global last_refresh
    now = datetime.now()
    delta = timedelta(minutes=3)
    elapsed = now - last_refresh
    if elapsed >= delta:
        if(debug):
            print ("full update")
        screen.update()
        last_refresh = datetime.now()
    else:
        if(debug):
            print ("partial update")
        screen.partial_update()

mqttclient = mqtt.Client(client_id=client_id)
mqttclient.username_pw_set(username="epaper", password="epaper")
mqttclient.on_connect = on_connect
mqttclient.on_message = on_message
mqttclient.connect(mqtthost, port, keepalive)

# Blocking call that processes network traffic, dispatches callbacks
# and handles reconnecting
# Other loop*() fucntions are available that give a threaded interface
# and a manual interface
try:
    mqttclient.loop_forever()

# deal with ^C
except KeyboardInterrupt:
    print("\ninterrupted!")

