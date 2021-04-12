# Firefly Chi Documentation
Firefly Chi is designed to be simple to understand, but for students without
strong software development skills it may still be daunting. Hopefully this
guide will clear some things up. Before you begin, try to read the
[short summary](summary.md) of this system so you understand what it *does* and
*doesn't* do.

## Setup and Usage
### On your own PC (development and testing)
1. Install Firefly Chi
If on linux/macos, install Firefly Chi by going to your favorite projects directory
and running `git clone https://github.com/CURocketEngineering/firefly_chi`. 
If on windows, you will likely like a client like 
[Github Desktop](https://desktop.github.com/). Setup is straightforward, just
install and follow the directions to download this project. 
2. Most basic dependency
For development, you will need a modern version of `Python3`. `Python3.8` and
further should work. On windows you can easily install python for free through 
the system shop. On linux, you'll need to use your package manager. 
3. Further dependencies
The only other dependency you *"need"* for development is python's `yaml`
module. `pip install pyyaml` should take care of it. Depending on what you're
testing you can try running `other/setup/setup-test.sh`. The rest of the system
should print out error messages if a dependency is missing for a plugin, but
it should continue working all other systems nonetheless. 
4. Test!
Run `python3 main.py` to start the system. Follow instructions below to modify
the configuration file.
### On a Raspberry Pi
For efficiency, the Raspberry Pi should probably run a headless version
of Raspbian/Raspberry Pi OS. You can easily follow a guide like
[this](https://howchoo.com/pi/install-raspberry-pi-os), just make sure to
download the headless iso to conserve battery life if used on an actual
rocket.
1. Install Firefly Chi
Log into the Pi and open a terminal. You can install Firefly Chi via git,
versioning software. If the folder `Documents` does not exist, simply
create it with `mkdir Documents`. Navigate inside `cd Documents` and install
Firefly Chi with `git clone https://github.com/CURocketEngineering/firefly_chi`.
Navigate inside `cd firefly_chi` and make sure everything is there `ls -la`.
2. Install dependencies
The Pi does not come with all of the dependencies needed for the system. To
install these, navigate to the `other/setup` directory and run the setup-pi
script `./setup-pi.sh`.
3. Configure the program
The configuration file used to define the system is `config/config.yaml`.
Modify this file to reflect any changes/desired settings for the flight system.
For instance, setting `main_altitude: 1500.0` to `main_altitude: 9500.0` will
make the `EJECT` state occur much higher for the second (main) parachute 
ejection.
4. Set up autorun
At this point, the Pi needs to start this system when it is first plugged in,
so we don't have to manually turn it on before putting it inside a rocket.
First run `sudo raspi-config` and change the settings to allow ssh and immediate
boot into user mode. Run `sudo rpi-update` and `sudo apt upgrade` to make sure
your software is up to date and will turn on without hdmi plugged in. No create
or edit the file `/etc/rc.local` (using nano, that's `sudo nano /etc/rc.local`).
Near the end, add the line
`cd /home/pi/Documents/firefly_chi && sudo -H -u pi /usr/bin/python3 main.py > /dev/null 2>&1 &`.
This ensures that after the Pi boots, it will enter into our programs folder
and run the system with full priveleges as the specified user. For the sake
of sanity when you reboot the system and need to use it, all output is ignored.
5. Test it!
At this point, your system should start when it is plugged in. If this is the 
case, you can check the `records` folder for flight logs after running it. If
developing, you can kill the process just like you'd kill any other.

## Developing
The *core system* contains how flight configurations are handled, the state system
used to control/define the flight of the rocket, and a system for handling
collected data. The *plugin system* was defined to keep anything unique or 
dynamic in each flight seperated. If changes/features for actions such as 
logging, telemetry, flight stabilization, data collection, etc are needed, this 
should be done in the form of a plugin for the system. 
### Core System
The core system is located in the `src/` directory. Information on each file
is [here](../../src/README.md). Each file is written in an object-oriented way
with classes that reflect the names of the file.
#### Editing the core system
Editing the core system should be done *very* carefully. After any change, make
sure to run the system with a simulation configuration in order to make sure
everything still operates as expected.
### Plugins
Plugins are found in the `plugins` directory. Not all plugins are executed when
the system starts. They are executed when the system reaches a state where a
`hook` is defined. Hooks consist of the state name along with the time of
execution in the format `<state_name>_<time>`. For example: `halt_start`,
`recover_start`, `upward_end`, and `eject_end`.
#### Creating a new plugin
Plugins can be written like any other python file. Simply define a function
inside a new file in `plugins` that accepts two arguments: `conf` and `dataobj`.
For example:
```python3
def test_plugin(conf, dataobj):
	print("Activating `test_plugin`")
	if conf.DEBUG:
		print("Current altitude is", dataobj.current_data["sensors"]["alt"])
```
`conf` is an object instance of the `src/Config.py` `Config` class and `dataobj`
is an object instance of the `src/Data.py` `Data` class.

To make the plugin callable, you must edit `plugins/__init__.py`. First, import
the correct file with something like `from . import test_plugin_file.py`.
Second, add the name of the plugin and the function to the `plugins` dictionary.
For instance, `"TestPlugin": test_plugin_file.test_plugin,`. 
#### Calling plugins
For a plugin to be called, you will need to define the time for a plugin to be
called along with the plugin name inside the current config file 
`config/config.yaml`. A plugins definition could look something like
```yaml
plugins:
  halt_start:
    - "FileSimulation"
    - "FileLogging"
  apogee_end:
    - "TestPlugin"
  recover_start:
    - "TestPlugin"
```
This means that Firefly Chi will execute `FileSimulation` and `FileLogging`
at the start of the `HALT` state (when the system starts). At the end of the
`APOGEE` state, the system will first call the `test_plugin(conf, dataobj)`
function. Also, at the start of `RECOVER` our new plugin will be called a
second time. A plugin can end and exit immediately or continue operating in
the background depending on how its made. 
#### New dependencies
If your new plugin or change to the system required a new python package that
is _not_ part of the standard library, make sure to add the instructions to
any documentation files or edit `other/setup/setup-test.sh` and 
`other/setup/setup-pi.sh` to reflect the necessary installation of another
dependency.

## Other Documentation
| Title                           | Description                      |
| :--                             | --:                              |
| [General](../README.md)         | Explanation of avionics.         |
| [Flight logic](logic.md)        | Explanation of flight logic.     |
| [Naming Conventions](naming.md) | Progress naming conventions.     |
| [Setup](setup.md)               | Setup procedure.                 |
| [Short Summary](summary.md)     | Simple description of project.   |
| [Hardware Table](hardware.md)   | Past and current hardware table. |

