# Logic
This file details the underlying logic of avionics.

### Purpose
Data collection, lighting ejection charges for parachutes, and telemetry.

### Measurements
* IMU - Measures gyro, acc, and magn for local accuracy (also calculates 
  pitch, yaw and roll)
* Barometer - Altitude (and pressure) used for the state system
* GPS - Measure latitude and longitude for global accuracy (also GPS altitude)

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
