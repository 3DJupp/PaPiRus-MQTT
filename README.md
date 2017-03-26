# PaPiRus-MQTT
MQTT Dashboard utilizing an ePaper / eInk Display on a Raspberry Pi (i prefer the Raspberry Pi Zero W, because i only need one cable)
![20170326_133457](https://cloud.githubusercontent.com/assets/8407566/24331707/3a2c4aba-123a-11e7-9441-34d822843e8c.jpg)

First, install the driver, install all necessary stuff and PaPiRus-MQTT.py to /home/pi
### Setup PaPiRus and PaPiRus-MQTT
```bash
curl -sSL https://goo.gl/ZOuov8 | sudo bash
```
###### Select your screen size
```bash
sudo papirus-set [1.44 | 1.9 | 2.0 | 2.6 | 2.7 ]
```  
or  
```bash
sudo papirus-config
```
Further information can be found on: https://github.com/PiSupply/PaPiRus

#### OpenHAB Items  
I use OpenHAB to push Data to my MQTT Broker  
Those items have i created for it (once they receive an update, it will be sent to the MQTT Broker)  
I recommend to Push the Data not to often, but at least once a minute (correct time on screen)
```java
Group 		e_paper  	  	"E Paper Display Items"				
Number		ep_power  	  	"Cumulated Wattage"		(e_paper)		{mqtt=">[openhab:epaper/power:state:*:default]"}
Number		ep_consumption		"Consumption 24h"		(e_paper)		{mqtt=">[openhab:epaper/cons_d:state:*:default]"}
Number		ep_consumption_hour	"Consumption 1h"		(e_paper)		{mqtt=">[openhab:epaper/cons_h:state:*:default]"}
Number		ep_temperature_indoor	"Cumulated Temperature Indoor"	(e_paper)		{mqtt=">[openhab:epaper/temp_indoor:state:*:default]"}
Number		ep_temperature_outdoor  "Cumulated Temperature Outdoor"	(e_paper)		{mqtt=">[openhab:epaper/temp_outdoor:state:*:default]"}
Number		ep_humidity_indoor  	"Cumulated Humidity Indoor"	(e_paper)		{mqtt=">[openhab:epaper/humi_indoor:state:*:default]"}
Number		ep_humidity_outdoor  	"Cumulated Humidity Outdoor"	(e_paper)		{mqtt=">[openhab:epaper/humi_outdoor:state:*:default]"}
Number		ep_download  	   	"Current Download"		(e_paper)		{mqtt=">[openhab:epaper/download:state:*:default]"}
Number		ep_upload  	    	"Current Upload"		(e_paper)		{mqtt=">[openhab:epaper/upload:state:*:default]"}
```

#### Autostart:  
Add this line to your /etc/rc.local right before the exit 0  
```bash
python /home/pi/PaPiRus-MQTT.py &
```
