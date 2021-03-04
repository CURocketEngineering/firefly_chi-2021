# Modules
Simple higher-level modules and logic.

## `Avionics.py`
A single point of accessing controlling the rocket. If another interface is
needed for a rocket, its design can be based off of `Avionics.py`. `Avionics.py`
also contains the *main loop* for running the rocket.

## `Config.py`
Configuration parser and handler for the rocket. 

## `State.py`
A system for changing state and activating any state-dependent hooks.

## `Data.py`
Data handling for the rocket. Can be interacted with to get and set data.
