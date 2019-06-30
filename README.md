# CURE Avionics vP
A python implementation of similar-functioning avionics code. Began in 2019.

## Goals
This is the 21st century. Batteries are cheap. So are computers. We can afford
to run a linux kernel on a rocket. The goals of this system are to 
1. **Be reusable**. We don't want to have to rewrite the codebase for different
microprocessors or components. 
2. **Be modular**. Both so multiple people can maintain different components of
the software and so each is easily understood and independent. 
3. **Be easy**. Everyone who's written hello world should be able to read the
higher-order files and understand what they actually do. This also implies 
*documentation*. 

## Setup
### Components
* A raspberry pi 3
* A raspberry pi sensehat
* A GlobalSat BU-353-S4 USB GPS Receiver 
[link](https://www.amazon.com/GlobalSat-BU-353-S4-USB-Receiver-Black/dp/B008200LHW/ref=sr_1_5?keywords=raspberry+pi+gps&qid=1561522641&s=gateway&sr=8-5)
* XBEE *Todo*
### Hardware
* Install raspbian on a raspberry pi (ideally headless)
* Clone this repo into a logical location 
* Run `source setup/setup.sh`
### Configuration
* Flight configuration files are located in `configs`

