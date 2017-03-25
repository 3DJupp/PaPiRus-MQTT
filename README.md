# PaPiRus-MQTT
MQTT Dashboard utilizing an ePaper / eInk Display
Energy/Smarthome Dashboard using the PaPiRus Zero on a Raspberry Pi Zero / Zero W
First, install the driver / example programs for the Pi-HAT

### Setup PaPiRus
###### Run this line and PaPiRus will be setup and installed
```curl -sSL https://goo.gl/i1Imel | sudo bash```
#### Getting Started
###### Select your screen size
```sudo papirus-set [1.44 | 1.9 | 2.0 | 2.6 | 2.7 ]```
or
```sudo papirus-config```
System will now reboot

Further information can be found on: https://github.com/PiSupply/PaPiRus

### Install PaPiRus MQTT

```bash
cd /tmp && wget https://bootstrap.pypa.io/get-pip.py && sudo chmod +x ./get-pip.py
./get-pip.py
pip install paho-mqtt

cd /home/pi && wget https://raw.githubusercontent.com/Dom1n1c/PaPiRus-MQTT/master/PaPiRus-MQTT.py && sudo chmod +x PaPiRus-MQTT.py

```

