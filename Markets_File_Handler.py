import csv
from csv import DictWriter
import os
import logging


class FileHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_file(self):
        try:
            # print(self.file_path)
            with open(self.file_path, 'r') as myfile:
                reader = csv.DictReader(myfile)
                return list(reader)
        except FileNotFoundError as e:
            logging.exception('No such file or directory', exc_info=True)
            return

    def add_to_file(self, new_value):  # dict or list
        fields = []
        if isinstance(new_value, dict):
            fields = new_value.keys()
            new_value = [new_value]
        elif isinstance(new_value, list):
            fields = new_value[0].keys()
        with open(self.file_path, 'a') as myfile:
            writer = DictWriter(myfile, fieldnames=fields, lineterminator='\n')
            if myfile.tell() == 0:
                writer.writeheader()
            writer.writerows(new_value)

    def clear(self):
        f = open(self.file_path, "w+")
        f.close()


class MarketsFileHandler(FileHandler):
    def __init__(self, file_path='AllMarkets.txt'):
        storage_path = f'Markets'
        if not os.path.exists(storage_path):
            os.mkdir(storage_path)
        self.file_path = 'Markets' + '/' + file_path
        super().__init__(self.file_path)


class MarketsProductsFileHandler(FileHandler):
    def __init__(self, file_path='0916249534'):
        storage_path = f'Markets/{file_path}'
        if not os.path.exists(storage_path):
            os.mkdir(storage_path)
        self.file_path = 'Markets' + '/' + file_path + '/' + 'products.txt'
        super().__init__(self.file_path)


# test2 = MarketsProductsFileHandler()
# test2.add_to_file({'sib': 1})


class MarketsCostumersFileHandler(FileHandler):
    def __init__(self, file_path='0916249534'):
        storage_path = f'Markets/{file_path}'
        if not os.path.exists(storage_path):
            os.mkdir(storage_path)
        self.file_path = 'Markets' + '/' + file_path + '/' + 'costumers.txt'
        super().__init__(self.file_path)


class MarketInvoicesFileHandler(FileHandler):
    def __init__(self, file_path='0916249534'):
        storage_path = f'Markets/{file_path}'
        if not os.path.exists(storage_path):
            os.mkdir(storage_path)
        self.file_path = 'Markets' + '/' + file_path + '/' + 'invoices.txt'
        super().__init__(self.file_path)


class MarketBlockCostumersFileHandler(FileHandler):
    def __init__(self, file_path='0916249534'):
        storage_path = f'Markets/{file_path}'
        if not os.path.exists(storage_path):
            os.mkdir(storage_path)
        self.file_path = 'Markets' + '/' + file_path + '/' + 'block_costumers.txt'
        super().__init__(self.file_path)

# test3 = MarketsCostumersFileHandler()
# test3.add_to_file({'username': '0123465846'})
#
# test = MarketsFileHandler('mahsa.txt')
# test.add_to_file({'mahsa': 'Aflaki'})
# print(test.read_file())
