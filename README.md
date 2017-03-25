# PaPiRus-MQTT
MQTT Dashboard utilizing an ePaper / eInk Display
Energy/Smarthome Dashboard using the PaPiRus Zero on a Raspberry Pi Zero / Zero W
First, install the driver / example programs for the Pi-HAT
https://github.com/PiSupply/PaPiRus

### Setup PaPiRus
###### Run this line and PaPiRus will be setup and installed
```curl -sSL https://goo.gl/i1Imel | sudo bash```
#### Getting Started
###### Select your screen size
```sudo papirus-set [1.44 | 1.9 | 2.0 | 2.6 | 2.7 ]```
or
```sudo papirus-config```
System will now reboot

### Install PIP and paho-mqtt

```bash
cd /tmp && wget https://bootstrap.pypa.io/get-pip.py && chmod +x ./get-pip.py
./get-pip.py
pip install paho-mqtt
```
