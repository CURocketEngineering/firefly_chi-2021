'''
plugins __init__.py
'''

from . import FileSimulation
# TODO import all plugins

plugins = {
    "FileLogging": None,
    "Xbee": None,
    "FileSimulation": FileSimulation.FileSimulation,
}
