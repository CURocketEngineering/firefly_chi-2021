# Firefly χ

![CURE LOGO](other/media/newlogo.png)

A Python implementation of similar-functioning avionics code designed to be
run on the avionics bay. Originally designed for the 2019-2020 Clemson
University Rocket Engineering year. The releases are considered functionally
complete.

This software suite is designed to work with a Raspberry Pi and Sense-Hat
with other specific components specified in the 
[documentation](other/documentation/README.md).

This is the 21st century. Batteries are cheap. So are computers. We can afford
to run a linux kernel on a rocket. The goals of this system are to 
1. **Be reusable**. We don't want to have to rewrite the codebase for different
microprocessors or components. 
2. **Be modular**. Both so multiple people can maintain different components of
the software and so each is easily understood and independent. 
3. **Be easy**. Everyone who's written hello world should be able to read the
higher-order files and understand what they actually do. This also implies 
_documentation_.

### Current Objectives

| Objective                        | Category   | Status      | Priority |
| ---                              | --:        | --:         | --:      |
| System Integrity & Unit Tests    | Testing    | Progress    | High     |
| Kalman Filter                    | Simulation | Progress    | Low      |

#### TODO
Remove from this list if the commit satisfies the requirement.
* [ ] Unit-tests should evaluate every core function at least once
  * [ ] A command-line option for running unit tests
* [ ] Finish simulation for custom kalman filter
* [ ] Rocket should recover itself if short happens restarting the raspberry pi
* [ ] GPS should record all possible measurements

## Contributing
Contributors who are new to github can read the 
[tutorial](other/documentation/tutorial/README.md).
Documentation for developing and usage guide can be read at
[simple documentation](other/documentation/README.md).
