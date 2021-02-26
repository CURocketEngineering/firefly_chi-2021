from time import sleep
from json import dumps

fl_dt = 0.2  # Log data 5 times per second

def FileLogger(conf, data):
    f = open("output.json", "w")
    try:
        while True:
            # Log 
            d = dumps(data.to_dict("?"))
            if d != "{}":
                f.write(d + "\n")
            # Sleep
            sleep(fl_dt)
    except:
        f.close()
