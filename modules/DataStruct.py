from json import dumps
from datetime import datetime

class DataStruct:
    def __init__(self,file_name):
        self.alt = 0 # unit ?
        self.acc_z = 0 # unit ?
        self.time = datetime.now()
        self._file = open(file_name,"a")

    def read_sensors(self):
        '''
        Updates data
        '''
        self.time = datetime.now()

    def to_json(self,state):
        '''
        Returns string of data
        '''
        # indent=None has no newlines (for parsing/space), indent=4 looks pretty
        return dumps(self.to_dict(state),indent=None) 

    
    def to_dict(self,state):
        '''
        Returns dict of data
        '''
        datajson = {
            "state": state,
            "time": str(self.time),
            "sensors" : {
                "alt" : self.alt,
            }
        }
        return datajson

    def write_out(self,state):
        self._file.write(self.to_json(state)+"\n")

    def process(self,state):
        return state
