'''
plugins __init__.py

Provides a mapping of plugin name to function.
'''

from . import FileSimulation
from . import SenseHatData
from . import USBGPS
from . import XbeeComm
from . import FileLogging
from . import USBRelay
from . import ActiveAero

UNIMPLEMENTED = lambda conf, data: None

plugins = {
    "FileLogging": FileLogging.FileLogger,
    "XbeeComm": XbeeComm.loop,
    "FileSimulation": FileSimulation.FileSimulation,
    "USBGPS": USBGPS.USBGPS,
    "SenseHatData": SenseHatData.SenseHatData,
    "USBRelayWatcher": USBRelay.RelayWatcher,
    "USBRelay1": USBRelay.Relay1,
    "USBRelay2": USBRelay.Relay2,
    "ActiveAero": ActiveAero.active_aero,
}
