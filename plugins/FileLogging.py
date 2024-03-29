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


from json import dumps
from os import path, makedirs
from time import sleep

FILELOGGING_DT = 0.2  # Log data 5 times per second
FILECLOSING_DT = 10  # Every 10 seconds, close and open file
REDUNDANCY_COUNT = 3  # Triple redundancy as per NASA https://llis.nasa.gov/lesson/18803
FILE_DIRECTORY = "records"

def FileLogger(conf, data):
    files = []
    # Make folder if not exists
    if not path.exists(FILE_DIRECTORY):
        makedirs(FILE_DIRECTORY)
    try:
        while True:
            # Open files
            files = []
            for i in range(REDUNDANCY_COUNT):
                modifier = str(i+1) if i > 0 else ""
                files.append(open(f"{FILE_DIRECTORY}/output{modifier}.json", "a"))
            # Log
            for i in range(int(FILECLOSING_DT/FILELOGGING_DT)):
                d = dumps(data.to_dict())
                for f in files:
                    if d != "{}":
                        f.write(d + "\n")
                # Sleep
                sleep(FILELOGGING_DT)
            # Close files
            for f in files:
                f.close()
    except Exception as e:
        for f in files:
            f.close()
        print("[FileLogging.py] (Files closed, logging stopped):", e)
        return
