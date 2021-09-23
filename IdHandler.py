# import os
#
# storage_path = 'info_files'
# if os.path.exists(storage_path):
#     print('Directory exist')
# else:
#     os.mkdir(storage_path)
#     print('Directory Created')
class Id:
    def __init__(self, file_path='id.txt'):
        self.file_path = file_path

    def get_id_s_a(self):
        try:
            with open(self.file_path, 'r') as myfile:
                id = int(myfile.read())
        except FileNotFoundError:
            id = 1010000
            print(id)
        finally:
            with open(self.file_path, 'w') as myfile:
                myfile.write(str(id + 1))
        return id

    def get_id_r_a(self):
        try:
            with open(self.file_path, 'r') as myfile:
                id = int(myfile.read())
        except FileNotFoundError:
            id = 1011000
            print(id)
        finally:
            with open(self.file_path, 'w') as myfile:
                myfile.write(str(id + 1))
        return id

    def get_id_s_s(self):
        try:
            with open(self.file_path, 'r') as myfile:
                id = int(myfile.read())
        except FileNotFoundError:
            id = 1210000
            print(id)
        finally:
            with open(self.file_path, 'w') as myfile:
                myfile.write(str(id + 1))
        return id

    def get_id_r_s(self):
        try:
            with open(self.file_path, 'r') as myfile:
                id = int(myfile.read())
        except FileNotFoundError:
            id = 1211000
            print(id)
        finally:
            with open(self.file_path, 'w') as myfile:
                myfile.write(str(id + 1))
        return id

    def get_id_s_h(self):
        try:
            with open(self.file_path, 'r') as myfile:
                id = int(myfile.read())
        except FileNotFoundError:
            id = 1110000
            print(id)
        finally:
            with open(self.file_path, 'w') as myfile:
                myfile.write(str(id + 1))
        return id

    def get_id_r_h(self):
        try:
            with open(self.file_path, 'r') as myfile:
                id = int(myfile.read())
        except FileNotFoundError:
            id = 1111000
            print(id)
        finally:
            with open(self.file_path, 'w') as myfile:
                myfile.write(str(id + 1))
        return id

# id = Id()
# print(id.get_id())
#
# test = FileHandler()
# test.add_to_file([{'name1': 'delaram', 'user1': "delaram"}, {'name1': 'kimia', 'user1': "kimia"}])
