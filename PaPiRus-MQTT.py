#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import paho.mqtt.client as mqtt
import time
from papirus import Papirus
from datetime import datetime
from datetime import timedelta
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import argparse

user = os.getuid()
if user != 0:
    print "Please run script as root"
    sys.exit()

papirus = Papirus()
papirus.clear()

power				= "0"
consumption			= "0"
temperature			= "0"
humidity			= "0"
temperature2		= "0"
humidity2			= "0"
download			= "0"
upload				= "0"
power_prev			= "0"
consumption_prev	= "0"
temperature_prev	= "0"
humidity_prev		= "0"
temperature2_prev	= "0"
humidity2_prev		= "0"
download_prev		= "0"
upload_prev			= "0"
last_refresh		= datetime.now()

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
# Subscribing in on_connect means that if we lose connection 
# and reconnect then subscriptions will be renewed
	client.subscribe([("epaper/power", 2), ("epaper/cons_d", 2), ("epaper/temp_indoor", 2), ("epaper/humi_indoor", 2), ("epaper/temp_outdoor", 2), ("epaper/humi_outdoor", 2), ("epaper/download", 2), ("epaper/upload", 2)])



def on_message(mqtt, obj, msg):
    global power, consumption, temperature, humidity, temperature2, humidity2, download, upload, power_prev, consumption_prev, temperature_prev, humidity_prev, temperature2_prev, humidity2_prev, download_prev, upload_prev

    if msg.topic == "epaper/power":
	power		= str(int(float(msg.payload)))
    if msg.topic == "epaper/cons_d":
	consumption 	= str(round(float(msg.payload), 3)).replace('.', ',')
    if msg.topic == "epaper/temp_indoor":
	temperature 	= str(round(float(msg.payload), 1)).replace('.', ',')
    if msg.topic == "epaper/humi_indoor":
	humidity 	= str(round(float(msg.payload), 1)).replace('.', ',')
    if msg.topic == "epaper/temp_outdoor":
	temperature2     = str(round(float(msg.payload), 1)).replace('.', ',')
    if msg.topic == "epaper/humi_outdoor":
	humidity2	= str(round(float(msg.payload), 1)).replace('.', ',')
    if msg.topic == "epaper/download":
	download	= str(round(float(msg.payload), 1)).replace('.', ',')
    if msg.topic == "epaper/upload":
	upload		= str(round(float(msg.payload), 1)).replace('.', ',')

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
	

def display_data():
    global power, consumption, temperature, humidity, temperature2, humidity2, download, upload, last_refresh
    image = Image.new('1', papirus.size, 1)
    draw = ImageDraw.Draw(image)

    font_path = "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"
    font_title = ImageFont.truetype(font_path, 17)
    font_values = ImageFont.truetype(font_path, 15)

    draw.text( (0,    0), "Smarthome ", font=font_title, fill=0)
    draw.text( (125,  0), (datetime.now().strftime("%H:%M")) + " Uhr", font=font_title, fill=0)
    draw.text( (0,   20), "Strom", font=font_values, fill=0)
    draw.text( (65,  20), power + " W ", font=font_values, fill=0)
    draw.text( (125, 20), consumption + " kWh", font=font_values, fill=0)
    draw.text( (0,   40), "Klima", font=font_values, fill=0)
    draw.text( (65,  40), temperature + " \xb0C ", font=font_values, fill=0)
    draw.text( (125, 40), humidity + " % RH", font=font_values, fill=0)
    draw.text( (0,   60), "Wetter", font=font_values, fill=0)
    draw.text( (65,  60), temperature2 + " \xb0C ", font=font_values, fill=0)
    draw.text( (125, 60), humidity2 + " % RH", font=font_values, fill=0)
    draw.text( (0,   80), "Internet", font=font_values, fill=0)
    draw.text( (65,  80), download + " DL", font=font_values, fill=0)
    draw.text( (125, 80), upload + " UL", font=font_values, fill=0)
    papirus.display(image)
    now = datetime.now()
    delta = timedelta(minutes=3)
    elapsed = now - last_refresh
    if elapsed >= delta:
        #print "Slept for 2 minutes"	
        papirus.update()
        last_refresh = datetime.now()
    else:
        #print "update"	
        papirus.partial_update()

client = mqtt.Client()
client.username_pw_set(username="epaper", password="epaper")
client.on_connect = on_connect
client.on_message = on_message
client.connect("10.0.0.1", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks
# and handles reconnecting
# Other loop*() fucntions are available that give a threaded interface
# and a manual interface

try:
	client.loop_forever()

# deal with ^C
except KeyboardInterrupt:
	print("\ninterrupted!")
