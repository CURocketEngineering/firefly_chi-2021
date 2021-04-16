# Logic
This file details the underlying logic of avionics.

### Purpose
This system exists for the purpose of data collection, lighting ejection
charges for parachutes, and telemetry. 

The plugin system provided by this software allows for communication between
systems on the rocket and access to our data and telemetry.

### Measurements
Most sensors (IMUs & barometers at least) are fundamentally the same on a physical
level. The differences are usually just manufacturer and library support. But the
same principals apply to all regardless of what name they go by.
* IMU - Measures gyro, acc, and magn for local accuracy (also calculates 
  pitch, yaw and roll (attitude))
  * The inertial measurement unit (also called 9dof for 9 degrees of freedom) 
	reads information for axes on a gyroscope, magnetometer, and accelerometer
  * Usually a library handles computing attitude from this, but if you're interested
	you can read the math on how this is done on
	[stack exchange](https://engineering.stackexchange.com/questions/3348/calculating-pitch-yaw-and-roll-from-mag-acc-and-gyro-data)
	or on other [educational sites](http://planning.cs.uiuc.edu/node103.html)
  * This data helps us understand the *orientation* of the rocket and what forces
	are acting on it from a perspective relative to the earth
* Barometer - Altitude (and pressure) used for the state system
  * Pressure and temperature are used to calculate altitude for systems
  * There are multiple ways to calculate altitude, our research showed that 
	different libraries (e.g. adafruit vs sparkfun) do this differently
    * For low altitudes, most libraries only rely on pressure and use math to 
	guess the altitude
	* So ultimately altitude isn't exact, but its good enough to get a relative
	  idea
    * Our system simply uses PV=nRT with a zeroed base pressure
  * In the end if somebody wants to calculate altitude differently post-flight,
	data for pressure and temperature are recorded so calculations can be redone
* GPS - Measure latitude and longitude for global accuracy (also GPS altitude)
  * GPS gets a lot of information from satellites
  * Phones don't use "GPS" like raw GPSs do, GPSs usually take a minute or two
    to find the satellites and get information
  * We simply parse the text of this information to get latitude, longitude, and
	altitude above the geoid of earth
  * GPS has more information too, some which may be useful, it is worth exploring
    in the future

## State-based systems
The rocket has states that effectively go in order, determining what it does
at any given moment.
1. HALT
Do nothing.
The `SenseHatData` plugin zeros the base pressure while in `HALT`.
2. ARM
Ready for liftoff. Must be triggered by a plugin (telemetry or simulation).
The `SimulationFile` plugin puts the rocket into arm after the first reading.
In order to jolt the rocket out of `HALT` and into `ARM`, the best way to do
this is via telemetry (see the `telemetry` repository). The `XbeeComm` plugin
accepts input that can arm the rocket.
3. UPWARD
Rocket is moving upward. Constantly checking for slowdown at apogee. This state
is triggered from `ARM` when the rocket is above 100 meters according to the
current data frame and the last 8 out of 10 pressure readings show an decrease in
pressure.
4. APOGEE
Rocket is at its peak. The ejection charge is lit. This state is triggered from
`UPWARD` when the rocket notices that the last 8 out of 10 pressure readings show
an increase in pressure.
5. DOWNWARD
Rocket is falling down. Constantly checking if below main parachute altitude.
6. EJECT
Rocket lights second ejection charge. This state is triggered when the rocket
falls below the `Config.MAIN_ALTITUDE` (meters).
7. RECOVERY
Rocket is still decending or already on the ground. Still sends telemetry.

## Implementation
In order to simplifiy development and updates in the future, all external devices
are moved to "plugins." So when the rocket changes states, it calls functions
listed in the config file as plugins.

### Hooks
Hooks are designed for plugins to be able to execute at specific times.
Most states have a pre and post hook `<state>_start` and `<state>_end`.
Other hooks can be added to the code. ex:
* `halt_start` - A hook that is executed when the system starts
* `eject_end` - A hook that is executed after the main (second) ejection

### Example
In the config file `config.yaml` you might see:
```
# Plugins start certain functions at different times
plugins:
  halt_start:
    - "FileSimulation"
    - "Xbee"
    - "FileLogging"
  apogee_start:
    - "USBRelay1"
  eject_start:
    - "USBRelay2"
```
This means that when the rocket starts and enters the `HALT` state, the
`FileSimulation`, `Xbee`, and `FileLogging` systems start. At apogee, 
the `USBRelay1` function is executed causing the first e-match to fire.
At the main ejection altitude, the second e-match fires thanks to `USBRelay2`.
But, since the only start plugin for data is `FileSimulation`, this is simply a 
simulation and should *not* be run on a launchpad.

## Layout of files in Firefly Chi
```
.
├── config - configuration files for the system
│   ├── config.yaml - current configuration file loaded
│   ├── irec2021.yaml - config file designed for IREC 2021
│   └── README.md
├── LICENSE - license for the software (MIT)
├── main.py - main program to be executed
├── other - files not involved in the execution of the program
│   ├── data - scripts and data for older systems
│   │   ├── old_data_reformatter.py
│   │   ├── old_irec2019.json
│   │   ├── README.md
│   │   └── sim_irec2019.json
│   ├── documentation - docs on how the system works
│   │   ├── hardware.md - list of avionics hardware
│   │   ├── logic.md - THIS FILE!!!
│   │   ├── README.md - information on this project as a whole
│   │   ├── setup.md - more information on how to set up the system
│   │   ├── summary.md - brief summaries on what this system is
│   │   └── tutorial - a directory explaining how to develop with github
│   ├── media - logos and other pictures
│   └── setup - information on how to set up the system
│       ├── README.md - explanation
│       ├── scripts - random scripts that can be called from others
│       │   ├── ip.py
│       │   └── welcome.py
│       ├── setup-pi.sh - script for setting up the raspberry pi
│       └── setup-test.sh - script for setting up a development environment
├── plugins - assorted plugins to simplify the system
│   ├── common - folder of submodules that can be used in other plugins
│   ├── FileLogging.py - plugin for logging data
│   ├── FileSimulation.py - plugin for simulating rocket flight
│   ├── __init__.py - contains information regarding plugin names
│   ├── low_level - folder with lower-level code for the higher-level plugins
│   ├── SenseHatData.py - reads data from rpi Sensehat
│   ├── USBGPS.py - reads data from a USB GPS
│   ├── USBRelay.py - handles accessing a USB Relay for ejection charges
│   └── XbeeComm.py - handles communication over Xbee
├── README.md - information on Firefly Chi
├── records - folder containing data logs in json format
└── src - source code for the core system
    ├── Avionics.py - holds the main loop for Firefly Chi
    ├── Config.py - handles reading the configuration file and parsing its data
    ├── Data.py - handles storing data
    ├── README.md - another explanation of these files
    └── State.py - handles the state system and calling plugin hooks
```
