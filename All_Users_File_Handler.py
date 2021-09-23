import csv
from csv import DictWriter


class UsersFileHandler:
    def __init__(self, file_path='All_users.txt'):
        self.file_path = file_path

    def read_file(self):
        try:
            with open(self.file_path, 'r') as myfile:
                reader = csv.DictReader(myfile)
                return list(reader)
        except FileNotFoundError as e:
            print(e)
            return

    def add_to_file(self, new_value):  # dict or list
        fields = []
        if isinstance(new_value, dict):
            fields = new_value.keys()
            new_value = [new_value]
        elif isinstance(new_value, list):
            fields = new_value[0].keys()
        with open( self.file_path, 'a') as myfile:

            writer = DictWriter(myfile, fieldnames=fields, lineterminator='\n')
            if myfile.tell() == 0:
                writer.writeheader()
            writer.writerows(new_value)

    def clear(self):
        f = open(self.file_path, "w+")
        f.close()




