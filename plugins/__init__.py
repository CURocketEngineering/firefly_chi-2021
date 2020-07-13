'''
plugins __init__.py

Provides a mapping of plugin name to function.
'''

from . import FileSimulation
from . import SenseHatData
from . import USBGPS

UNIMPLEMENTED = lambda x,y: None

plugins = {
    "FileLogging": UNIMPLEMENTED,
    "Xbee": UNIMPLEMENTED,
    "FileSimulation": FileSimulation.FileSimulation,
    "USBGPS": USBGPS.USBGPS,
    "SenseHatData": SenseHatData.SenseHatData,
    "USBRelay": UNIMPLEMENTED,
}
