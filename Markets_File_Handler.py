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
# ----------------------------------------------
#     def read_file(self):
#         try:
#             # print(self.file_path)
#             with open(self.file_path, 'r') as myfile:
#                 reader = csv.DictReader(myfile)
#                 return list(reader)
#         except FileNotFoundError as e:
#             logging.exception('No such file or directory', exc_info=True)
#             return
#
#     def add_to_file(self, new_value):  # dict or list
#         fields = []
#         if isinstance(new_value, dict):
#             fields = new_value.keys()
#             new_value = [new_value]
#         elif isinstance(new_value, list):
#             fields = new_value[0].keys()
#         with open(self.file_path, 'a') as myfile:
#             writer = DictWriter(myfile, fieldnames=fields, lineterminator='\n')
#             if myfile.tell() == 0:
#                 writer.writeheader()
#             writer.writerows(new_value)
#
#     def clear(self):
#         f = open(self.file_path, "w+")
#         f.close()
#
#     def update(self, new_values):
#         f = open(self.file_path, "w+")
#         f.close()
#         FileHandler.add_to_file(self, new_values)
#
#     def show_table(self):
#         with open(self.file_path) as f:
#             my_table = from_csv(f)
#         print(my_table)
#
#
# class MarketsFileHandler(FileHandler):
#     def __init__(self, file_path='AllMarkets.txt'):
#         storage_path = f'Markets'
#         if not os.path.exists(storage_path):
#             os.mkdir(storage_path)
#         self.file_path = 'Markets' + '/' + file_path
#         super().__init__(self.file_path)
#
#
# class MarketsProductsFileHandler(FileHandler):
#     def __init__(self, file_path='0916249534'):
#         storage_path = f'Markets/{file_path}'
#         if not os.path.exists(storage_path):
#             os.mkdir(storage_path)
#         self.file_path = 'Markets' + '/' + file_path + '/' + 'products.txt'
#         super().__init__(self.file_path)
#
#
# # test2 = MarketsProductsFileHandler()
# # test2.add_to_file({'sib': 1})
#
#
# class MarketsCostumersFileHandler(FileHandler):
#     def __init__(self, file_path='0916249534'):
#         storage_path = f'Markets/{file_path}'
#         if not os.path.exists(storage_path):
#             os.mkdir(storage_path)
#         self.file_path = 'Markets' + '/' + file_path + '/' + 'costumers.json'
#         super().__init__(self.file_path)
#
#
# class MarketInvoicesFileHandler(FileHandler):
#     def __init__(self, file_path='0916249534'):
#         storage_path = f'Markets/{file_path}'
#         if not os.path.exists(storage_path):
#             os.mkdir(storage_path)
#         self.file_path = 'Markets' + '/' + file_path + '/' + 'invoices.txt'
#         super().__init__(self.file_path)
#
#     def show_tale(self):
#         with open(self.file_path) as f:
#             my_table = from_csv(f)
#         print(my_table)
#
#
# class MarketBlockCostumersFileHandler(FileHandler):
#     def __init__(self, file_path='0916249534'):
#         storage_path = f'Markets/{file_path}'
#         if not os.path.exists(storage_path):
#             os.mkdir(storage_path)
#         self.file_path = 'Markets' + '/' + file_path + '/' + 'block_costumers.txt'
#         super().__init__(self.file_path)
#
#
