from Markets_File_Handler import *
from product import Product
from All_Users_File_Handler import UsersFileHandler
import logging
from prettytable import from_csv
from prettytable import PrettyTable
# from purchase_invoices import Invoice
import datetime
from datetime import time
from invoice import Invoice

logging.basicConfig(filename='log.log', filemode='a', level=logging.DEBUG,
                    format='%(asctime)s - %(process)d - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


def convert_string_to_dict(dict_list_string):
    def convert(lst):
        res_dct = {lst[item_]: lst[item_ + 1] for item_ in range(0, len(lst), 2)}
        return res_dct

    a, a2, b = [], [], []
    temp = dict_list_string.split("},{")
    for i, item in enumerate(temp):
        temp[i] = item.split("'")
    for j in temp:
        a2 = []
        for i, item in enumerate(j):
            if i % 2 != 0:
                a2.append(item)
        a.append(a2)
    for item in a:
        b.append(convert(item))
    return b


def show_table(file_path):
    with open(file_path) as f:
        my_table = from_csv(f)
    print(my_table)


def show_table2(list_dict):
    my_table = PrettyTable()
    my_table.field_names = list(list_dict[0].keys())
    temp = []
    for item in list_dict:
        temp.append(list(item.values()))
    my_table.add_rows(temp)
    print(my_table)


def show_factor(list_dict):
    dict_ = list_dict[0]
    x = PrettyTable()
    x3 = PrettyTable()
    products = dict_['products']
    x3.field_names = ['products_name', 'brand', 'single_price', 'count', 'price']
    temp = []
    for item in products:
        temp.append([item['product'], item['brand'], item['single_price'], item['count'], item['price']])
    x3.add_rows(temp)
    x.field_names = ["Market name", "Costumer", "date", "total price", 'products']
    x.add_row([dict_['market_name'], dict_['costumer_phone'], dict_['date'], dict_['total_price'], x3])
    print(x)


def not_block(costumer, list_dict):
    for item in list_dict:
        if item['username'] == costumer and item['status'] == 'active':
            return True


class Market:
    def __init__(self, username, password, market_name, start, end):
        self.username = username
        self.password = password
        self.market_name = market_name
        self.start = start
        self.end = end
        self.costumers = []
        self.block_customers = []
        self.products = []
        self.invoices = []
        self.save()

    def save(self):
        user = UsersFileHandler()
        user.add_to_file({'username': self.username, 'password': self.password, 'type': 'Manager'})
        file_info = FileHandler()
        file_info.add_to_file(self.__dict__)
        pass

    @staticmethod
    def add_product(market_name, product_name, brand, product_count, product_price, barcode, expiration_date):
        product = Product(product_name, brand, product_count, product_price, barcode, expiration_date)
        all_info = FileHandler().read()
        products_file = all_info[market_name]['products']
        products_file.append(product.__dict__)
        FileHandler().update(all_info)

    @staticmethod
    def view_list_of_products(market_name):
        products_list = FileHandler().read()[market_name]['products']
        if products_list:
            show_table2(products_list)
        else:
            print('There is no products to show')
            logging.info('Try to read not exist file (products.txt)')

    @staticmethod
    def inventory_alert(market_name):
        products_list = FileHandler().read()[market_name]['products']
        if products_list:
            temp = []
            for item in products_list:
                if int(item['product_count']) <= 5:
                    temp.append(item)
            if temp:
                x = PrettyTable()
                x.field_names = temp[0].keys()
                for item in temp:
                    x.add_row(item.values())
                print("This products are out of range: ")
                print(x)
            else:
                print('No products are being finished')
        else:
            print('There is no product to check!')
            logging.info('Try to read not exist file (products.txt)')

    @staticmethod
    def customer_purchase_invoices(market_name):
        customers_invoices_list_dict = FileHandler().read()[market_name]['invoices']
        if customers_invoices_list_dict:
            for item in customers_invoices_list_dict:
                # show_table2([item])
                show_factor([item])
                print()
        else:
            print('There is no factors to show')
            logging.info('Try to read not exist file (invoices.txt)')

    @staticmethod
    def invoice_search(market_name, customer_phone='', date='', until_date=''):
        def search_by_phone(customer_phone_, all_invoice_list):
            filtered_invoice_list = []
            if customer_phone_:
                for invoice_ in all_invoice_list:
                    if customer_phone_ in invoice_['costumer_phone']:
                        filtered_invoice_list.append(invoice_)
                return filtered_invoice_list
            else:
                return all_invoice_list

        def search_by_date(date_, all_invoice_list):
            filtered_invoice_list = []
            if date_:
                for invoice_ in all_invoice_list:
                    if invoice_['date'] == date_:
                        filtered_invoice_list.append(invoice_)
                return filtered_invoice_list
            else:
                return all_invoice_list

        def search_by_until_date(date_u, all_invoice_list):
            filtered_invoice_list = []
            if date_u:
                for invoice_ in all_invoice_list:
                    if invoice_['date'] <= date_u:
                        filtered_invoice_list.append(invoice_)
                return filtered_invoice_list
            else:
                return all_invoice_list

        # customer_file = MarketsCostumersFileHandler(username)
        # invoice_file = MarketInvoicesFileHandler(username)
        # customer_file_path = customer_file.file_path
        # invoice_file_path = invoice_file.file_path
        invoices_list = FileHandler().read()[market_name]['invoices']
        # if os.path.exists(customer_file_path) and os.path.exists(invoice_file_path):
        # all_invoice_list = invoice_file.read_file()
        if date:
            invoices = search_by_date(date, search_by_phone(customer_phone, invoices_list))
        else:
            invoices = search_by_until_date(until_date, search_by_phone(customer_phone, invoices_list))
        if invoices:
            [show_table2([item]) for item in invoices]
        else:
            print('No data matched to your order!')

    # else:
    #     print('There is No Costumers or invoices')
    #     logging.info('Try to read not exist file (costumers.json)')

    @staticmethod
    def customer_list(market_name):  # just phone number and status(block/active)
        customer_file = FileHandler().read()[market_name]['costumers']
        if customer_file:
            table = PrettyTable(['num','costumers PhoneNumber'])
            temp = []
            for i,item in enumerate(customer_file , start=1):
                temp.append([i,item])
            table.add_rows(temp)
            print(table)
            return True
        else:
            print('There is No Costumer')
            logging.info('Try to read not exist file (costumers.json)')

    #
    @staticmethod
    def show_customers_info(market_name):  # phone number, status, its invoices
        all_info = FileHandler().read()
        customers_list = all_info[market_name]['costumers']
        invoice_list = all_info[market_name]['invoices']
        if customers_list:
            for i, customer_ in enumerate(customers_list, start=1):
                print(f"{i}. Customer Phone_Number: {customer_}")
                for invoice_ in invoice_list:
                    if invoice_['costumer_phone'] == customer_:
                        show_factor([invoice_])
                print(u'\u2500' * 70)
        else:
            print('There is No Costumer')
            logging.info('Try to read not exist file (costumers.json)')

    #
    @staticmethod
    def block_customer(market_name, costumer):
        all_info = FileHandler().read()
        block_costumers_list = all_info[market_name]['block_customers']
        all_costumers_list = all_info[market_name]['costumers']
        if costumer in all_costumers_list and costumer not in block_costumers_list:
            block_costumers_list.append(costumer)
            FileHandler().update(all_info)
        else:
            print('This costumer is blocked since before!')

    #
    # def save(self):
    #     user = UsersFileHandler()
    #     user.add_to_file({'username': self.username, 'password': self.password, 'type': 'Manager'})
    #     file_info = FileHandler()
    #     file_info.add_to_file(self.__dict__)
    #     pass
    #
    @staticmethod
    def find_product_by_name_and_brand(market_name, product_name='', brand=''):
        products_list = FileHandler().read()[market_name]['products']
        temp_list = []
        for item in products_list:
            if f'{product_name}{brand}' in f'{item["product_name"]}{item["brand"]}':
                temp_list.append(item)
        if temp_list:
            show_table2(temp_list)
            return True
        else:
            print('There is no product matched to your order!')

    #
    # @staticmethod
    # def find_product_by_barcode(market_username, barcode):
    #     products_file_handler = MarketsProductsFileHandler(market_username)
    #     products_list = products_file_handler.read_file()
    #     for item in products_list:
    #         if item['barcode'] == barcode:
    #             return item
    #
    @staticmethod
    def check_inventory(market_name, product_name, brand, count):
        products_list = FileHandler().read()[market_name]['products']
        product = {}
        temp = {}
        for item in products_list:
            if f'{product_name} {brand}' == f'{item["product_name"]} {item["brand"]}':
                # print(item)
                product = item
                break
        if product:
            if int(count) <= int(product['product_count']):
                temp['product'] = product['product_name']
                temp['brand'] = product['brand']
                temp['single_price'] = product['product_price']
                temp['count'] = count
                temp['price'] = int(count) * int(product['product_price'])
                return temp
        else:
            print('This product is not available')

    # @staticmethod
    # def update_products(market_username, product, new_value):
    #     products_file_handler = MarketsProductsFileHandler(market_username)
    #     products_object_list = products_file_handler.read_file()
    #     for item in products_object_list:
    #         if item['barcode'] == product['barcode']:
    #             item = new_value
    #             break
    #     products_file_handler.update(products_object_list)

    # @staticmethod
    # def insert_costumer(username, costumer_phone):
    #     temp_dict = {}
    #     temp_dict['username'] = costumer_phone
    #     temp_dict['status'] = 'active'
    #     costumer_file = MarketsCostumersFileHandler(username)
    #     costumer_file.add_to_file(temp_dict)
    #
    @staticmethod
    def shopping(market_name, costumer_phone, shopping_list):
        # product_list:[{ products_name |  brand   | single_price | count | price }]
        all_info = FileHandler().read()
        market = all_info[market_name]

        def update_product_after_shopping(shopping_list_):
            products_list = market['products']
            error = False
            for item1 in shopping_list_:
                number_of_requests, product_name, brand = item1['count'], item1['product'], item1['brand']
                for item in products_list:
                    if f"{item['product_name']} {item['brand']}" == f"{product_name} {brand}":
                        if int(item['product_count']) < int(number_of_requests):
                            print(f'Inventory for the product: "{product_name}" less than your request')
                            error = True
            if not error:
                for item1 in shopping_list_:
                    number_of_requests, product_name, brand = item1['count'], item1['product'], item1['brand']
                    for item in products_list:
                        if f"{item['product_name']} {item['brand']}" == f"{product_name} {brand}":
                            item['product_count'] = int(item['product_count']) - int(number_of_requests)
                            # print(10, item['product_count'])

                invoice = Invoice(market_name, costumer_phone, shopping_list)
                market['invoices'].append(invoice.__dict__)
                if costumer_phone not in market['costumers']:
                    market['costumers'].append(costumer_phone)
                # print(11, market)
                FileHandler().update(all_info)
                return True

        update_product_after_shopping(shopping_list)

    @staticmethod
    def view_the_list_of_active_stores():
        all_markets_info = FileHandler().read()
        # all_markets_list = all_markets_file.read_file()
        now = datetime.datetime.now()
        now = time(now.hour, now.minute, now.second)
        temp_store = []
        for item in all_markets_info.keys():
            store_opening = all_markets_info[item]['start']
            store_closing = all_markets_info[item]['end']
            # print(now)
            if store_opening <= str(now) < store_closing:
                temp_store.append(
                    {'Market Name': all_markets_info[item]['market_name'],
                     'Start Working': all_markets_info[item]['start'], 'End Working': all_markets_info[item]['end']})
        if temp_store:
            show_table2(temp_store)

    @staticmethod
    def market_search(string):
        all_markets_info = FileHandler().read()
        # all_markets_list = all_markets_file.read_file()
        temp = []
        for item in all_markets_info.keys():
            if string in item:
                temp.append({'Market Name': all_markets_info[item]['market_name'],
                             'Start Working': all_markets_info[item]['start'],
                             'End Working': all_markets_info[item]['end']})
        if temp:
            show_table2(temp)
            return temp

    @staticmethod
    def market_accurate_search(string, customer_username):
        all_markets_info = FileHandler().read()
        if string in all_markets_info.keys():
            if customer_username not in all_markets_info[string]['block_customers']:
                temp = {'Market Name': all_markets_info[string]['market_name'],
                        'Start Working': all_markets_info[string]['start'],
                        'End Working': all_markets_info[string]['end']}
                return temp
            else:
                print('You are block :) ')
                return False
        print('No Market with this name were found ')
        return False

    @staticmethod
    def get_market_name(market_username):
        all_markets_info = FileHandler().read()
        # print(0, all_markets_info)
        for item in all_markets_info.keys():
            # print(1, item)
            # print(2, type(market_username))
            # print(3, type(item['market_name']))
            if market_username == all_markets_info[item]['username']:
                market_name = all_markets_info[item]['market_name']
                return market_name
        # print(f'There is no Market by name {market_name}')

# ===================================================================================
# a = datetime.datetime.strptime('12:12:12', '%H:%M:%S').strftime('%H:%M:%S')
# now = datetime.datetime.now()
# now = time(now.hour, now.minute, now.second)
# # print(now > a)
# a = []
# # a.append(1, 2, 3)
# print(a)
# # datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')
# # time.hour
#
# # @staticmethod
# # def update(object,**kwargs1,**kwargs2 ):
# #     list_dict = object.read_file()
# #     found = True
# #     for item in list_dict:
# #         for key, value in kwargs1.items():
# #             if item[key] != value:
# #                 found = False
# #                 break
# #         if found:
# #             for key, value in kwargs1.items():
# #                 item[key] = kwargs2[key]
# #             break
#
#
# # def search_by_date_and_phone(customer_phone, date):
# #     factors_list = []
# #     invoice_list = invoice_file.read_file()
# #     for invoice_ in invoice_list:
# #         if f'{customer_phone + date}' in f"{invoice_['costumer_name']} + {invoice_['date']}":
# #             factors_list.append(invoice_)
# #     return factors_list
# #
# # def search_by_until_date_and_phone(customer_phone, date):
# #     factors_list = []
# #     invoice_list = invoice_file.read_file()
# #     for invoice_ in invoice_list:
# #         if invoice_['costumer_name'] == customer_phone and invoice_['date'] <= date:
# #             factors_list.append(invoice_)
# #     return factors_list

# def __init__(self, username, password, market_name, start, end):
# test = Market('1', '1', 'Niloofar', '12:00:00', '24:00:00')
# test.add_product_list('nili', 'milk', 'mihan', 20, 2000, '123', '12/12/12')


# tesy = {'nili': {'username': '1', 'password': '1', 'market_name': 'nili', 'start': '12:00:00', 'end': '24:00:00',
#                  'costumers': [], 'block_customers': ['09111111111'], 'products': [], 'invoices': []},
#         'Niloofar': {'username': '1', 'password': '1', 'market_name': 'Niloofar', 'start': '12:00:00',
#                      'end': '24:00:00', 'costumers': [], 'block_customers': [], 'products': [], 'invoices': []},
#         'Negin': {'username': '09333333333',
#                   'password': '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',
#                   'market_name': 'Negin', 'start': '07:00:00', 'end': '24:00:00', 'costumers': [],
#                   'block_customers': [], 'products': [], 'invoices': []}}
#

# for key in tesy.keys():
#     print(tesy[key])
