# Setup
## Components
* A Raspberry Pi 3
* A Raspberry Pi Sense HAT
* A GlobalSat BU-353-S4 USB GPS Receiver 
[link](https://www.amazon.com/GlobalSat-BU-353-S4-USB-Receiver-Black/dp/B008200LHW/ref=sr_1_5?keywords=raspberry+pi+gps&qid=1561522641&s=gateway&sr=8-5)
* XBEE *Todo*
## Hardware
* Install headless raspbian on a raspberry pi
* Put an empty `ssh` in root (`boot`) (`touch ssh`)
* Boot (wait 5 minutes to allow ssh)
* Somehow find out the ip address of the pi
* `ssh pi@ip` with password `raspberry`
* Clone this repo into a logical location
* Run `source setup/setup.sh`
* Run `sudo raspi-config`
  * Allow ssh and boot straight to user 
* Run `sudo rpi-update`
  * May not be necessary, but will allow rpi to turn on without hdmi plugged in
* Run `sudo apt upgrade` to make sure packages are up-to-date
* Set up the autorun file in `/etc/rc.local`
  * Add the line `cd /home/pi/Documents/firefly_chi && sudo -H -u pi /usr/bin/python3 main.py > /dev/null 2>&1 &`
### Configuration
* Flight configuration files are located in `configs`
* The current configuration should replace `config.json`
  * ex// `cp configs/test.json config.json`
