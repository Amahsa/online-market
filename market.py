from Markets_File_Handler import *
from product import Product
from All_Users_File_Handler import UsersFileHandler

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
        all_products_list = products_file.read_file()
        if not all_products_list:
            print('there is no product to show!')
        else:
            show_table(all_products_list)

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
        customers_invices_file = MarketInvoicesFileHandler(username)
        all_customers_list = customers_invices_file.read_file()
        show_table(all_customers_list)

    @staticmethod
    def invoice_search(username):
        customer_file = MarketInvoicesFileHandler(username)
        all_customers_list = customer_file.read_file()

    @staticmethod
    def customer_list(username):
        customer_file = MarketsCostumersFileHandler(username)
        all_customers_list = customer_file.read_file()
        if not all_customers_list:
            print('There is No Costumer')
            return False
        show_table(all_customers_list)
        return True

    @staticmethod
    def block_customer(username, costumer):
        block_costumers = MarketBlockCostumersFileHandler(username)
        block_costumers.add_to_file(costumer)

    def save(self):
        user = UsersFileHandler()
        user.add_to_file({'username': self.username, 'password': self.password, 'type': 'Manager'})
        file_info = MarketsFileHandler()
        file_info.add_to_file(self.__dict__)
        pass


def show_table(list_dict):
    header = list(list_dict[0].keys())
    print('\n' + u'\u2500' * 22 * len(header))
    print('|' + ' ' * 4, end='')
    for item in header:
        print(item.center(20, ' '), end='|')
    print('\n' + u'\u2500' * 22 * len(header))
    for i, item in enumerate(list_dict):
        print('|' + str(i+1).center(3, ' ') + '|', end='')
        values = item.values()
        for val in values:
            if isinstance(val, list):
                show_table(val)
            elif isinstance(val,str):
                print(val.center(20, ' '), end='|')
        print('\n' + u'\u2500' * 22 * len(header))
