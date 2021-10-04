import logging
from prettytable import from_csv
from prettytable import PrettyTable
from All_Users_File_Handler import UsersFileHandler
import datetime
from invoice import Invoice
import Customer_File_Handler

logging.basicConfig(filename='log.log', filemode='a', level=logging.DEBUG,
                    format='%(asctime)s - %(process)d - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


# Read the file and display it
def show_table(file_path):
    with open(file_path) as f:
        my_table = from_csv(f)
    print(my_table)


# Display input data as a table
def show_table2(list_dict):
    my_table = PrettyTable()
    my_table.field_names = list(list_dict[0].keys())  # heads
    temp = []
    for item in list_dict:
        temp.append(list(item.values()))  # rows
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


class Customer:
    def __init__(self, first_name, last_name, username, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.cart = {}
        self.previous_invoices = []
        self.save()

    @staticmethod
    def view_previous_invoices(username):
        costumer_invoices_file = Customer_File_Handler.CostumerFileHandler().read()  # Fetch all customers
        info = costumer_invoices_file[username]  # Fetch the desired customer
        list_invoices = info['previous_invoices']  # Fetch customer purchase invoices
        if list_invoices:
            show_table2(list_invoices)
        else:
            print('There is no factors to show')
            logging.info('Try to read not exist file (invoices.txt)')

    @staticmethod
    def insert_to_cart(costumer_username, market_name, product):
        costumers = Customer_File_Handler.CostumerFileHandler().read()  # Fetch all customers
        costumer = costumers[costumer_username]  # Fetch the desired customer
        cart = costumer['cart']  # Fetch customer purchase cart
        if market_name in list(cart.keys()):  # If the shopping cart is not empty
            cart[market_name].append(product)
        else:
            cart[market_name] = []
            cart[market_name].append(product)
        Customer_File_Handler.CostumerFileHandler().update(costumers)

    @staticmethod
    def view_pre_invoice(costumer_username, market_name):
        costumers = Customer_File_Handler.CostumerFileHandler().read()
        costumer = costumers[costumer_username]
        cart = costumer['cart'][market_name]
        if cart != [None] and cart != []:
            show_table2(cart)
            return cart

    @staticmethod
    def edit_pre_invoice(costumer_username, market_name):
        costumers = Customer_File_Handler.CostumerFileHandler().read()
        costumer = costumers[costumer_username]
        cart = costumer['cart'][market_name]
        for i, item in enumerate(cart):
            print(U"\u2500" * 50)
            show_table2([item])
            # print(item)
            print(U"\u2500" * 50)
            new_value = input(
                'Enter new count or Enter r for remove it or just press Enter (new count|r|press Enter): ')
            if new_value:
                if new_value.isdigit():
                    if int(new_value) > 0:
                        item['count'] = new_value
                        item['price'] = int(new_value) * int(item['single_price'])
                    else:
                        print('The count must be grater than zero')
                elif new_value == 'r':
                    cart.pop(i)

        Customer_File_Handler.CostumerFileHandler().update(costumers)

    @staticmethod
    def invoicing(market_name, costumer_phone, product):
        date = datetime.datetime.now()
        total_price = 0
        for item in product:
            total_price += item['price']
        invoice = {}
        invoice['market_name'] = market_name
        invoice['costumer_phone'] = costumer_phone
        invoice['product'] = product
        invoice['date'] = date
        invoice['total_price'] = total_price

    @classmethod
    def confirm_purchase(cls, costumer_username, market_name):
        costumers = Customer_File_Handler.CostumerFileHandler().read()
        costumer = costumers[costumer_username]
        costumer_market_cart = costumer['cart'][market_name]
        # Build a purchase invoice
        invoice = Invoice(market_name, costumer_username, costumer_market_cart)
        # Add pre-invoice to customer invoices
        invoices = costumers[costumer_username]['previous_invoices']
        invoices.append(invoice.__dict__)
        # Clear Shopping Cart and Update Costumers info file
        costumer['cart'][market_name] = []
        Customer_File_Handler.CostumerFileHandler().update(costumers)

    def save(self):
        user = UsersFileHandler()
        user.add_to_file({'username': self.username, 'password': self.password, 'type': 'Customer'})
        file_info = Customer_File_Handler.CostumerFileHandler()
        file_info.add_to_file(self.__dict__)
        pass
