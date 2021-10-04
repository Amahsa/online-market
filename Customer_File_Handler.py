import json
import os


class CostumerFileHandler():
    def __init__(self, path='costumers.json'):
        self.path = path

    def add_to_file(self, new_value):
        if os.path.exists(self.path):
            with open(self.path) as fp:
                listObj = json.load(fp)
                listObj[new_value["username"]] = new_value
        else:
            listObj = {}
            listObj[new_value["username"]] = new_value
        with open(self.path, 'w') as json_file:
            json.dump(listObj, json_file, indent=4)

    def update(self, new_value):
        with open(self.path, 'w') as json_file:
            json.dump(new_value, json_file, indent=4)

    def read(self):
        with open(self.path, 'r') as fp:
            obj = json.load(fp)
            return obj
