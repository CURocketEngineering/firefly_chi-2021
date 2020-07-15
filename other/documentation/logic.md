# Logic

## So you want to make an avionics bay?
### Purpose

### Measurements

### Parachutes

### Telemetry

### More Measurements

## State-based systems


## Implementation
### Hooks
Hooks are designed for plugins to be able to execute at specific times.
Most states have a pre and post hook `<state>_start` and `<state>_end`.
Other hooks can be added to the code. A list of available custom hooks
is below:
* `eject_now` - A hook for when the parachute needs to immediately eject
