# Functionality
## Pre-flight
Before flight, the system will be able to complete the following actions
with xbee communication. 
* Calculate air-break speeds/timing table
* Change configuration files
* Arm
* Run any command-line action
* Pull data
Any of these actions are also able to be completed by SSHing into the py.

## Flight 
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
 
## Post-flight
When the system has detected that it is no longer in any flight state and is 
instead ready to be recovered, it will display the following in a repeated
sequence. 
1. State [Recover]
2. Max Altitude (ft)
3. Max Velocity (ft/s)
