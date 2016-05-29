import json


class Survey(object):
    def __init__(self):
        with open('survey.json') as json_data:
            d = json.load(json_data)
            json_data.close()
            self.data = d

    def get_trace(self):
        pass
