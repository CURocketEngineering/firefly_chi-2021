"""
ActiveAero.py
=============
Incomplete plugin for connecting the active aero system to firefly chi.
"""
import serial

def active_aero(conf, dataobj):
    """
    Run the loop for managing active aero UART.
    """
    ser = serial.Serial('/dev/ttyS0', 9600, timeout=5)  # AMA0?
    # FYI: If you use another medium to connect systems you may need to see
    # the code for reading USBs in the other plugins (XBee and USBGPS)
    line = "1"
    rpi_data = dataobj.current_data  # dictionary of data
    # Add data to sensors
    rpi_data["sensors"]["uart_code"] = "AABB"
    while True and not conf.shutdown:
        if line != "end":
            line = ser.readline().decode('utf-8').rstrip()
            elements = line.split()
            rpi_data["sensors"]["uart_info"] = {}
            rpi_data["sensors"]["uart_info"]["time"] = elements[0]
            rpi_data["sensors"]["uart_info"]["2"] = elements[0] 
            print(line)
        else:
            ser.write(b"Hello from Raspberry Pi\n")
            break
