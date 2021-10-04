import os
import logging
import json


class FileHandler:
    def __init__(self, path='market_managers.json'):
        self.path = path

    def add_to_file(self, new_value):
        if os.path.exists(self.path):
            with open(self.path) as fp:
                listObj = json.load(fp)
                listObj[new_value["market_name"]] = new_value
        else:
            listObj = {}
            listObj[new_value["market_name"]] = new_value
        with open(self.path, 'w') as json_file:
            json.dump(listObj, json_file, indent=5)

    def update(self,new_value):
        with open(self.path, 'w') as json_file:
            json.dump(new_value, json_file, indent=5)

    def read(self):
        try:
            with open(self.path, 'r') as fp:
                obj = json.load(fp)
                return obj
        except FileNotFoundError as e:
            logging.exception('No such file or directory', exc_info=True)
            return
