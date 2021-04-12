'''
UART.py
'''
import serial

def uart(conf, dataobj):
    ser = serial.Serial('/dev/ttyS0', 9600, timeout=5)  # AMA0?
    line = "1"
    rpi_data = dataobj.current_data  # dictionary of data
    # Add data to sensor
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
