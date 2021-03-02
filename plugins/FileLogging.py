"""
FileLogging.py
==============
Main file logging.

Recommendation:
If this is ever picked back up, I recommend splitting logging into main and
secondary. Main for time, altitude, gps, etc. Secondary for time, imu readings,
misc. GPS readings, and anything else. Same reasons as before, but I also think 
having secondary readings (or even all readings) at a different rate than the
most important data would allow anyone to modify write speeds to favor more
demanding data analysis. More data = more accurate flight analysis. - Harrison
"""

from time import sleep
from json import dumps

filelogging_dt = 0.2  # Log data 5 times per second
fileclosing_dt = 10  # Every 10 seconds, close and open file
redundancy_count = 3  # Triple redundancy as per NASA https://llis.nasa.gov/lesson/18803

def FileLogger(conf, data):
    files = []
    try:
        while True:
            # Open files
            files = []
            for i in range(redundancy_count):
                modifier = str(i) if i > 0 else ""
                files.append(open(f"output{modifier}.json", "w"))
            # Log
            for i in range(int(fileclosing_dt/filelogging_dt)):
                d = dumps(data.to_dict())
                for f in files:
                    if d != "{}":
                        f.write(d + "\n")
                # Sleep
                sleep(filelogging_dt)
            # Close files
            for f in files:
                f.close()
    except Exception as e:
        for f in files:
            f.close()
        print("[FileLogging.py] (Files closed, logging stopped):", e)
        return
