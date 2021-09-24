from Markets_File_Handler import *
from product import Product
from All_Users_File_Handler import UsersFileHandler
import logging
from prettytable import from_csv
from prettytable import PrettyTable
from purchase_invoices import invoice
import datetime

logging.basicConfig(filename='log.log', filemode='a', level=logging.DEBUG)


def convert_string_to_dict(dict_list_string):
    def convert(lst):
        res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
        return res_dct

    a, a2, b = [], [], []
    temp = dict_list_string.split("},{")
    for i, item in enumerate(temp):
        temp[i] = item.split("'")
    for j in temp:
        for i, item in enumerate(j):
            if i % 2 != 0:
                a2.append(item)
        a.append(a2)
    for item in a:
        b.append(convert(item))
    return b


def show_table2(file_path):
    # print(file_path)
    with open(file_path) as f:
        my_table = from_csv(f)
    print(my_table)


def show_factor(list_dict):
    dict = list_dict[0]
    x = PrettyTable()
    x2 = PrettyTable()
    x3 = PrettyTable()
    products = convert_string_to_dict(dict['product'])
    x3.field_names = ['products_name', 'brand', 'single_price', 'count', 'price']
    for item in products:
        x3.add_row([item['product'], item['brand'], item['single_price'], item['count'], item['price']])
    x.field_names = ["Market name", "Costumer", "date", "total price", 'products']
    x.add_row([dict['market_name'], dict['costumer_name'], dict['date'], dict['total_price'], x3])
    print(x)


def show_table(list_dict):
    try:
        header = list(list_dict[0].keys())
        print('\n' + u'\u2500' * 22 * len(header))
        print('|' + ' ' * 4, end='')
        for item in header:
            print(item.center(20, ' '), end='|')
        print('\n' + u'\u2500' * 22 * len(header))
        for i, item in enumerate(list_dict):
            print('|' + str(i + 1).center(3, ' ') + '|', end='')
            values = item.values()
            for val in values:
                if isinstance(val, list):
                    show_table(val)
                elif isinstance(val, str):
                    print(val.center(20, ' '), end='|')
            print('\n' + u'\u2500' * 22 * len(header))
    except TypeError:
        print('Nothing to show!')
        logging.warning('Try to open a not existed file')


def show_invoice(list_dict):
    try:
        list_ = list_dict[0]
        print('\n' + u'\u2500' * 21 * 5)
        print('|' + ' ' * 4, end='')
        print('Market Name:'.center(16, " "), list_['market_name'].center(16, ' '), end='|')
        print('Costumer Name:'.center(16, " "), list_['costumer_name'].center(16, ' '), end='|')
        print('Date:'.center(16, " "), list_['date'].center(16, ' '), end='|')
        a = []
        a2 = []
        temp = list_['product'].split("},{")
        for i, item in enumerate(temp):
            temp[i] = item.split("'")
        for j in temp:
            for i, item in enumerate(j):
                if i % 2 != 0:
                    a2.append(item)
            a.append(a2)

        def convert(lst):
            res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
            return res_dct

        b = []
        for item in a:
            b.append(convert(item))
        show_table(b)
        print('|' + f"total price: '{list_['total_price']}".center(105, ' ') + '|', end='')
        print('\n' + u'\u2500' * 21 * 5)
    except TypeError:
        print('Nothing to show!')
        logging.warning('Try to open a not existed file')

def find_costumer(costumer,path):
    pass

class Market:
    def __init__(self, username, password, market_name, start, end):
        self.username = username
        self.password = password
        self.market_name = market_name
        self.start = start
        self.end = end
        self.save()

    @staticmethod
    def register_product_list(username, product_name, brand, product_count, product_price, barcode, expiration_date):
        product = Product(product_name, brand, product_count, product_price, barcode, expiration_date)
        products_file = MarketsProductsFileHandler(username)
        products_file.add_to_file(product.__dict__)

    @staticmethod
    def inventory(username):
        products_file = MarketsProductsFileHandler(username)
        file_path = products_file.file_path
        show_table2(file_path)
        # all_products_list = products_file.read_file()
        # if not all_products_list:
        #     print('there is no product to show!')
        # else:
        #     show_table(all_products_list)

    @staticmethod
    def inventory_alert(username):
        products_file = MarketsProductsFileHandler(username)
        all_products_list = products_file.read_file()
        temp = []
        for item in all_products_list:
            if int(item['product_count']) <= 5:
                temp.append(item)
        if temp:
            print("This products aren out of range: ")
            show_table(temp)

    @staticmethod
    def customer_purchase_invoices(username):  # فاکتور خرید مشتری ها
        customers_invoices_file = MarketInvoicesFileHandler(username)
        list_dict = customers_invoices_file.read_file()
        # file_path = customers_invoices_file.file_path
        for item in list_dict:
            show_factor(list_dict)
            print()

        # all_customers_invoices = customers_invoices_file.read_file()
        # show_invoice(all_customers_invoices)

    @staticmethod
    def invoice_search(username):
        customer_file = MarketInvoicesFileHandler(username)
        all_customers_list = customer_file.read_file()

    @staticmethod
    def customer_list(username):
        customer_file = MarketsCostumersFileHandler(username)
        # file_path = customer_file.file_path
        # show_table2(file_path)
        all_customers_list = customer_file.read_file()
        if not all_customers_list:
            print('There is No Costumer')
            return False
        show_table(all_customers_list)
        return True

    @staticmethod
    def block_customer(username, costumer):
        block_costumers = MarketBlockCostumersFileHandler(username)
        path = block_costumers.path
        if not find_costumer(costumer, path):
            temp_dict = {}
            temp_dict['costumer_username'] = costumer
            block_costumers.add_to_file(temp_dict)
        else:
            print('This costumer is locked since before!')


    def save(self):
        user = UsersFileHandler()
        user.add_to_file({'username': self.username, 'password': self.password, 'type': 'Manager'})
        file_info = MarketsFileHandler()
        file_info.add_to_file(self.__dict__)
        pass

    @staticmethod
    def find_product_by_NameAndBrand(market_username, products_name, brand):
        products_file_handler = MarketsProductsFileHandler(market_username)
        products_list = products_file_handler.read_file()
        for item in products_list:
            if item.product_name == products_name and item.brand == brand:
                return item

    @staticmethod
    def find_product_by_Barcode(market_username, barcode):
        products_file_handler = MarketsProductsFileHandler(market_username)
        products_list = products_file_handler.read_file()
        for item in products_list:
            if item.product_name == barcode:
                return item



    @staticmethod
    def update_products(market_username, product, new_value):
        products_file_handler = MarketsProductsFileHandler(market_username)
        products_object_list = products_file_handler.read_file()
        for item in products_object_list:
            if item['barcode'] == product['barcode']:
                item = new_value
                break
        products_file_handler.update(products_object_list)

    @staticmethod
    def shopping(market_username, costumer_username, shopping_list, total_price):
        # product_list:[{ products_name |  brand   | single_price | count | price }]
        def update_product_after_shopping(market_username, shopping_list):
            products_file_handler = MarketsProductsFileHandler(market_username)
            products_object_list = products_file_handler.read_file()
            for item1 in shopping_list:
                count, products_name, brand = item1['count'], item1['products_name'], item1['brand']
                for item in products_object_list:
                    if item['product_name'] == products_name and item['brand'] == brand:
                        if int(item['count']) >= int(count):
                            item['count'] = int(item['count'])
                            item['count'] -= int(count)

            products_file_handler.clear()
            products_file_handler.add_to_file(products_object_list)

        update_product_after_shopping(market_username, shopping_list)
        invoice_file_handler = MarketInvoicesFileHandler(market_username)
        now = datetime.datetime.now()
        market_invoice = invoice(market_name=market_username, costumer_name=costumer_username,
                                 product=shopping_list, date=now, total_price=total_price)
        invoice_file_handler.add_to_file(market_invoice)
