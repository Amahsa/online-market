from Markets_File_Handler import *
from product import Product
from All_Users_File_Handler import UsersFileHandler
import logging
from prettytable import from_csv
from prettytable import PrettyTable
from purchase_invoices import Invoice
import datetime

logging.basicConfig(filename='log.log', filemode='a', level=logging.DEBUG,
                    format='%(asctime)s - %(process)d - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


def convert_string_to_dict(dict_list_string):
    def convert(lst):
        res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
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


def show_factor(list_dict):
    dict = list_dict[0]
    x = PrettyTable()
    x2 = PrettyTable()
    x3 = PrettyTable()
    products = convert_string_to_dict(dict['product'])
    x3.field_names = ['products_name', 'brand', 'single_price', 'count', 'price']
    temp = []
    for item in products:
        temp.append([item['product'], item['brand'], item['single_price'], item['count'], item['price']])
    x3.add_rows(temp)
    x.field_names = ["Market name", "Costumer", "date", "total price", 'products']
    x.add_row([dict['market_name'], dict['costumer_name'], dict['date'], dict['total_price'], x3])
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
        self.save()

    @staticmethod
    def register_product_list(username, product_name, brand, product_count, product_price, barcode, expiration_date):
        product = Product(product_name, brand, product_count, product_price, barcode, expiration_date)
        products_file = MarketsProductsFileHandler(username)
        products_file.add_to_file(product.__dict__)

    @staticmethod
    def view_inventory(username):
        products_file = MarketsProductsFileHandler(username)
        file_path = products_file.file_path
        if os.path.exists(file_path):
            show_table(file_path)
        else:
            print('There is no products to show')
            logging.info('Try to read not exist file (products.txt)')

    @staticmethod
    def inventory_alert(username):
        products_file = MarketsProductsFileHandler(username)
        if os.path.exists(products_file.file_path):
            all_products_list = products_file.read_file()
            temp = []
            for item in all_products_list:
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
    def customer_purchase_invoices(username):
        customers_invoices_file = MarketInvoicesFileHandler(username)
        list_dict = customers_invoices_file.read_file()
        if os.path.exists(customers_invoices_file.file_path):
            for item in list_dict:
                show_factor([item])
                print()
        else:
            print('There is no factors to show')
            logging.info('Try to read not exist file (invoices.txt)')

    @staticmethod
    def invoice_search(username, customer_phone='', date='', until_date=''):
        def search_by_phone(customer_phone, all_invoice_list):
            filtered_invoice_list = []
            if customer_phone:
                for invoice_ in all_invoice_list:
                    if customer_phone in invoice_['costumer_name']:
                        filtered_invoice_list.append(invoice_)
                return filtered_invoice_list
            else:
                return all_invoice_list

        def search_by_date(date, all_invoice_list):
            filtered_invoice_list = []
            if date:
                for invoice_ in all_invoice_list:
                    if invoice_['date'] == date:
                        filtered_invoice_list.append(invoice_)
                return filtered_invoice_list
            else:
                return all_invoice_list

        def search_by_until_date(date, all_invoice_list):
            filtered_invoice_list = []
            if date:
                for invoice_ in all_invoice_list:
                    if invoice_['date'] <= date:
                        filtered_invoice_list.append(invoice_)
                return filtered_invoice_list
            else:
                return all_invoice_list

        customer_file = MarketsCostumersFileHandler(username)
        invoice_file = MarketInvoicesFileHandler(username)
        customer_file_path = customer_file.file_path
        invoice_file_path = invoice_file.file_path

        if os.path.exists(customer_file_path) and os.path.exists(invoice_file_path):

            all_invoice_list = invoice_file.read_file()
            invoices = ''
            if date:
                invoices = search_by_date(date, search_by_phone(customer_phone, all_invoice_list))
            else:
                invoices = search_by_until_date(until_date, search_by_phone(customer_phone, all_invoice_list))
            if invoices:
                [show_factor([item]) for item in invoices]
            else:
                print('No data matched to your order!')
        else:
            print('There is No Costumers or invoices')
            logging.info('Try to read not exist file (costumers.txt)')

    @staticmethod
    def customer_list(username): # just phone number and status(block/active)
        customer_file = MarketsCostumersFileHandler(username)
        file_path = customer_file.file_path
        if os.path.exists(file_path):
            show_table(file_path)
            return True
        else:
            print('There is No Costumer')
            logging.info('Try to read not exist file (costumers.txt)')

    @staticmethod
    def show_customers_info(username): # phone number, status, its invoices
        customer_file = MarketsCostumersFileHandler(username)
        invoice_file = MarketInvoicesFileHandler(username)
        file_path = customer_file.file_path
        if os.path.exists(file_path):
            customers_list = customer_file.read_file()
            invoice_list = invoice_file.read_file()
            for i, customer_ in enumerate(customers_list, start=1):
                print(f"{i}. Customer Phone_Number: {customer_['username']} | status: {customer_['status']}")
                for invoice_ in invoice_list:
                    if invoice_['costumer_name'] == customer_['username']:
                        show_factor([invoice_])
                print(u'\u2500' * 70)
        else:
            print('There is No Costumer')
            logging.info('Try to read not exist file (costumers.txt)')


    @staticmethod
    def block_customer(market, costumer):
        block_costumers_file = MarketBlockCostumersFileHandler(market)
        all_costumers_file = MarketsCostumersFileHandler(market)
        list_dict = block_costumers_file.read_file()
        if not_block(costumer, all_costumers_file.read_file()):
            temp_dict = {}
            temp_dict['costumer'] = costumer
            block_costumers_file.add_to_file(temp_dict)
            # update(block_costumers,'costomer',costumer,'status','block')
        else:
            print('This costumer is blocked since before!')

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
    def find_product_by_barcode(market_username, barcode):
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
    def insert_costumer(username, costumer_user_name):
        temp_dict = {}
        temp_dict['username'] = costumer_user_name
        temp_dict['status'] = 'active'
        costumer_file = MarketsCostumersFileHandler(username)
        costumer_file.add_to_file(temp_dict)

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
        market_invoice = Invoice(market_name=market_username, costumer_name=costumer_username,
                                 product=shopping_list, date=now, total_price=total_price)
        invoice_file_handler.add_to_file(market_invoice)




        # @staticmethod
        # def update(object,**kwargs1,**kwargs2 ):
        #     list_dict = object.read_file()
        #     found = True
        #     for item in list_dict:
        #         for key, value in kwargs1.items():
        #             if item[key] != value:
        #                 found = False
        #                 break
        #         if found:
        #             for key, value in kwargs1.items():
        #                 item[key] = kwargs2[key]
        #             break



        # def search_by_date_and_phone(customer_phone, date):
        #     factors_list = []
        #     invoice_list = invoice_file.read_file()
        #     for invoice_ in invoice_list:
        #         if f'{customer_phone + date}' in f"{invoice_['costumer_name']} + {invoice_['date']}":
        #             factors_list.append(invoice_)
        #     return factors_list
        #
        # def search_by_until_date_and_phone(customer_phone, date):
        #     factors_list = []
        #     invoice_list = invoice_file.read_file()
        #     for invoice_ in invoice_list:
        #         if invoice_['costumer_name'] == customer_phone and invoice_['date'] <= date:
        #             factors_list.append(invoice_)
        #     return factors_list
