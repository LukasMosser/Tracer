import json
import numpy as np

class Survey(object):
    def __init__(self):
        with open('data.json') as json_data:
            d = json.load(json_data)
            d = np.array(d)
            json_data.close()
            self.data = np.divide(d, max(np.abs(d.flatten())))

    def get_trace(self):
        pass
