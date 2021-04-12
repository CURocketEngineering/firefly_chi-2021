# Summary of the system
Depending on your level of familiarity with the system, these summaries should
provide more insight into what the system does and how the system works.

## Basic Summary
Firefly χ is a student researched and developed flight system for rocket used
by Clemson University Rocket Engineering (CURE). At its core, the system monitors 
the state of the rocket (HALTed, ARMed for takeoff, going UPWARD, at APOGEE, 
DOWNWARD, second EJECtion, and during RECOVERy) and handles the data (altimeter, 
IMU, and GPS) collected during flight. The system is designed and tested to be 
run on a Raspberry Pi 3.

## Intermediate details
*Most* flights by CURE require more advanced activity. The system needs to 
collect and record data, provide ejection charges during the correct moments,
and provide monitorable telemetry via a radio system. Code and logic for this
is located in the `plugins` directory, as opposed to the `src` directory for
the core system. Since we want this system to be reusable with minimal effort,
configuring launches with different plugins and other flight settings is done
by editing the file `config/config.yaml`.

## Advanced details
While the system is tested on a Raspberry Pi 3 with SenseHat, it can be easily
be ran on other computers for developmental purposes. On top of this, for flight
the system should be easily modifiable for other hardware. Plugins are 
encapsulated by being threaded at the time of each hook call. 
