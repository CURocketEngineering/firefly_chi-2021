"""Print IP Address to shell and sensehat."""

from sense_hat import SenseHat
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
print(ip)
SenseHat().show_message(ip)

