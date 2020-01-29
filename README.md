# CURE Avionics
A Python implementation of similar-functioning avionics code designed to be
run on the avionics bay. Originally designed for the 2019-2020 Clemson
University Rocket Engineering year.

This software suite is designed to work with a Raspberry Pi and Sense-Hat
with other specific components specified in the 
[documentation](documentation/README.md). 
Components be easily changed by modifying [low_level](modules/low_level) 
classes.

## Goals
This is the 21st century. Batteries are cheap. So are computers. We can afford
to run a linux kernel on a rocket. The goals of this system are to 
1. **Be reusable**. We don't want to have to rewrite the codebase for different
microprocessors or components. 
2. **Be modular**. Both so multiple people can maintain different components of
the software and so each is easily understood and independent. 
3. **Be easy**. Everyone who's written hello world should be able to read the
higher-order files and understand what they actually do. This also implies 
_documentation_.

### Current Status
The current status is `Golden Golden 1`. 

### Current Objectives

| Objective                           | Category      | Status      | Priority |
| ---                                 | --:           | --:         | --:      |
| SSH over Xbee                       | Communication | Not Started | Low      |
| Sensehat Interface                  | Setup         | Not Started | High     |
| System Integrity Test               | Testing       | Not Started | High     |
| Recover flight data from damaged SD | Simulation    | Halted      | Medium   |
| Finish Flight Simulation            | Simulation    | Progress    | High     |
| Kalman Filter                       | Simulation    | Progress    | High     |
| Structural Design - Fall            | Structure     | Started     | High     |
| Stuctural Design - IREC             | Strucutre     | Not Started | Low      |
| Cameras                             | Cameras       | Not Started | Medium   |
| Unit Testing                        | Testing       | Not Started | Medium   |
| Relay Test                          | Testing       | Not Started | Medium   |
| XBee Distance Test                  | Testing       | Not Started | Medium   |
