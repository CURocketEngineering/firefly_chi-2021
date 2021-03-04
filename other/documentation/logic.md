# Logic
This file details the underlying logic of avionics.

### Purpose
Data collection, lighting ejection charges for parachutes, and telemetry.

### Measurements
* IMU - Measures gyro, acc, and magn for local accuracy (also calculates 
  pitch, yaw and roll)
* Barometer - Altitude (and pressure) used for the state sys tem
* GPS - Measure latitude and longitude for global accuracy

## State-based systems
The rocket has states that effectively go in order, determining what it does
at any given moment.
1. HALT
Do nothing.
2. ARM
Ready for liftoff. Must be triggered by a plugin (telemetry or simulation).
3. UPWARD
Rocket is moving upward. Constantly checking for slowdown at apogee.
4. APOGEE
Rocket is at its peak. The ejection charge is lit.
5. DOWNWARD
Rocket is falling down. Constantly checking if below main parachute altitude.
6. EJECT
Rocket lights second ejection charge.
7. RECOVERY
Rocket is still decending or already on the ground. Still sends telemetry.

## Implementation
In order to simplifiy development and updates in the future, all external devices
are moved to "plugins." So at different times of the rocket

### Hooks
Hooks are designed for plugins to be able to execute at specific times.
Most states have a pre and post hook `<state>_start` and `<state>_end`.
Other hooks can be added to the code. ex:
* `halt_start` - A hook that is executed when the system starts
* `eject_end` - A hook that is executed after the main (second) ejection
