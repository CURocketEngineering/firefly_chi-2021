# CURE Avionics vP
A python implementation of similar-functioning avionics code. Began in 2019.

## Functionality
### Pre-flight
Before flight, the system will be able to complete the following actions
without xbee communication (input from sensehat). 
* Calculate air-break speeds/timing table
* Change configuration files
* Arm
Before flight, the system will be able to complete the following actions
with xbee communication. 
* Calculate air-break speeds/timing table
* Change configuration files
* Arm
* Run any command-line action
* Pull data
Any of these actions are also able to be completed by SSHing into the py.
### Flight 
If `Arm` is initiated and anything is wrong with the system, the display and 
speaker will emit a message. If the system is flight ready it will perform the 
following. 
* Communicate data/state information via xbee
* Use the following state system to perform actions
  1. Arm 
     * Wait for the rocket to launch, or be manually forced into ignite
     * Averages current altitude to provide relative altitude measurements
  2. Ignite
     * Begin formal data collection/communication
  3. Burn
     * Record/communicate data as the rocket continues to accelerate
  4. Coast
     * Record/communicate data as the rocket loses acceleration and coasts
     * Detect when the rocket is approaching zero speed and begins to fall
  5. Apogee
     * Eject drogue parachute (by lighting e-matches) with the setting from `config.json`
  6. Fall
     * Record/communicate data as the rocket coasts downward
     * Detect when the rocket is approaching main altitude as specified in 
     `config.json`
  7. Eject
     * Eject main parachute (by lighting e-matches) with the setting from `config.json`
  8. Recover
     * Record/communicate data as the rocket lands and is waiting to be recovered
* The following meta-states exist for emergency and debug circumstances
  1. Halt
     * Quit all actions
  2. Restart
     * Restart the system
  3. Shutdown
     * Shutdown the system
  4. Test
     * Make sure the system is ready to be used
### Post-flight
When the system has detected that it is no longer in any flight state and is 
instead ready to be recovered, it will display the following in a repeated
sequence. 
1. State [Recover]
2. Max Altitude (ft)
3. Max Velocity (ft/s)

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
### 2019-2020 CURE-goals
* Reformat/recover past flight data into correct json format (for testing)
* Make sure gps and xbee work with fin-tennas
* Configure air-break simulation into program
* Write comm-program
* Write telemetry program
* Write sensehat display/config program

## Setup
### Components
* A raspberry pi 3
* A raspberry pi sensehat
* A GlobalSat BU-353-S4 USB GPS Receiver 
[link](https://www.amazon.com/GlobalSat-BU-353-S4-USB-Receiver-Black/dp/B008200LHW/ref=sr_1_5?keywords=raspberry+pi+gps&qid=1561522641&s=gateway&sr=8-5)
* XBEE *Todo*
### Hardware
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
### Configuration
* Flight configuration files are located in `configs`
* The current configuration should replace `config.json`
