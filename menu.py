import logging
from market import Market
from customer import Customer
from All_Users_File_Handler import UsersFileHandler
import sys
import hashlib
import re

logging.basicConfig(level=logging.DEBUG, filename='Log.log', filemode='a',
                    format='%(asctime)s - %(process)d - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


def password_hashing(password):
    hashed_password = hashlib.sha256(password.encode())
    return hashed_password.hexdigest()


def validation_phone_number(phone_number):
    regex = '^(\s)*09\d{9}$'
    if re.search(regex, phone_number):
        return True


def validation_password(password):
    regex = '[\w\d]{6}[\w\d]*'
    if re.search(regex, password):
        return True


def validation_time(time_):
    regex = '^\d{2}:\d{2}:\d{2}\s*$'
    if re.search(regex, time_):
        return True


def user_not_taken(username):
    all_users_file = UsersFileHandler()
    all_users = all_users_file.read_file()
    not_found = True
    if all_users:
        for item in all_users:
            if item['username'] == username:
                not_found = False
                return not_found
        if not_found:
            return True
    return True


def user_info(username):
    all_users = UsersFileHandler()
    for item in all_users.read_file():
        if item['username'] == username:
            return item


def add_product(market_name):
    continue_ = 'y'
    while continue_ == 'y':
        product_name = input('product name : ')
        brand = input('brand : ')
        product_count = input('count : ')
        product_price = input('price : ')
        barcode = input('barcode : ')
        expiration_date = input('expiration date (dd-mm-yyyy): ')
        Market.add_product(market_name=market_name, product_name=product_name, brand=brand,
                           product_count=product_count, product_price=product_price, barcode=barcode,
                           expiration_date=expiration_date)
        logging.info(f"A market manager added a product")
        continue_ = input('continue to add product (y/n)? ').lower()


def main_menu():
    print(U"\u2500" * 50)
    print(' ' * 20 + '1. Sign up')
    print(' ' * 20 + '2. Sign in')
    print(' ' * 20 + '3. Exit')
    print(U"\u2500" * 50)
    item = input('Chose an item: ')
    if item == '1':
        register()
    elif item == '2':
        sign_in()
    elif item == '3':
        sys.exit()
    else:
        main_menu()


def register_manager():
    market_name, start_working, end_working, password = '', '1', '0', '0'
    phone_number = input('Phone number (this will be use as your username): ')
    while not validation_phone_number(phone_number):
        print('Enter valid phone number!')
        phone_number = input('Phone number (this will be use as your username): ')
    username = phone_number
    if user_not_taken(username):
        while not validation_password(password):
            password = input('Password : ')
            temp = input('Repeat password : ')
            if temp != password:
                print('Error')
                while temp != password:
                    password = input('password : ')
                    temp = input('Repeat password : ')
        while not market_name:
            market_name = input('Market name : ')
        while not start_working or not end_working or end_working < start_working:
            while not validation_time(str(start_working)):
                start_working = input('Opening time (Use 24-hour format hh:mm:ss ): ')
            while not validation_time(str(end_working)):
                end_working = input('Closing time (Use 24-hour format hh:mm:ss): ')

        Market(username, password_hashing(password), market_name, start_working, end_working)
        logging.info(f"A manager by username:{username} is signed up")
    else:
        print('You registered by this phone number since before!')
        logging.info(f"Try to re-register by username:{username}")


def register():
    print(' ' * 20 + '1. Market manager')
    print(' ' * 20 + '2. Customer')
    print(' ' * 20 + '3. Exit')
    item = input('Chose an item: ')
    if item == '1':
        register_manager()
        main_menu()
    elif item == '2':
        register_customer()
        main_menu()
    elif item == '3':
        sys.exit()
    else:
        register()


def sign_in():
    username = input('Username : ')
    password = input('Password : ')
    user = user_info(username)
    if user:
        if user['password'] == password_hashing(password):
            if user['type'] == 'Customer':
                logging.info(f"A costumer by username:{user['username']} signed in")
                customer_menu(user['username'])
            elif user['type'] == 'Manager':
                try:
                    Market.inventory_alert(Market.get_market_name(username))
                except TypeError:
                    logging.exception('error in showing inventory', exc_info=True)
                logging.info(f"A manager by username:{user['username']} signed in")
                market_manager_menu(Market.get_market_name(username))
        else:
            print('Incorrect password ')
            logging.warning(f"A user by username:{user['username']} entered incorrect password")
            sign_in()
    else:
        print('No user found! please sign up or check the username')
        logging.warning(f"Try to sign in with unavailable  username:{username}")
        main_menu()


def market_manager_menu(username):
    print(U"\u2500" * 50)
    print(' Manager Menu '.center(50, U"\u2500"))
    print(' ' * 20 + '1. add product')
    print(' ' * 20 + '2. View list of Products')
    print(' ' * 20 + '3. Check unavailable products')
    print(' ' * 20 + '4. View All invoices')
    print(' ' * 20 + '5. Invoice search')
    print(' ' * 20 + '6. View all costumers and their invoices')
    print(' ' * 20 + '7. View list of all costumers')
    print(' ' * 20 + '8. Block a costumer')
    print(' ' * 20 + '9. Back to main menu')
    print(' ' * 20 + '10. Exit')
    print(U"\u2500" * 50)
    item = input('Chose an item: ')
    if item == '1':
        add_product(username)
        market_manager_menu(username)
    elif item == '2':
        Market.view_list_of_products(username)
        market_manager_menu(username)
    elif item == '3':
        Market.inventory_alert(username)
        market_manager_menu(username)
    elif item == '4':
        Market.customer_purchase_invoices(username)
        market_manager_menu(username)
    elif item == '5':
        customer_phone = input('Enter customer phone number or press Enter')
        date = input('Enter date or press Enter')
        until_date = input('Enter date or press Enter')
        Market.invoice_search(username, customer_phone, date, until_date)
        market_manager_menu(username)
    elif item == '6':
        Market.show_customers_info(username)
        market_manager_menu(username)
    elif item == '7':
        Market.customer_list(username)
        market_manager_menu(username)
    elif item == '8':
        customer_exist = Market.customer_list(username)
        if customer_exist:
            costumer = input('Which costumer do you want to block? (Enter Username)')
            Market.block_customer(username, costumer)
            print(f'The user {costumer} blocked successfully')
            market_manager_menu(username)
        market_manager_menu(username)
    elif item == '9':
        main_menu()
    elif item == '10':
        sys.exit()


def register_customer():
    first_name = input('First Name: ')
    last_name = input('Last Name: ')
    phone_number = input('Phone number (this will be use as your username): ')
    while not validation_phone_number(phone_number):
        print('Enter valid phone number!')
        phone_number = input('Phone number (this will be use as your username): ')
    username = phone_number
    if user_not_taken(username):
        password = ''
        while not validation_password(password):
            password = input('Password : ')
            temp = input('Repeat password : ')
            if temp != password:
                print('Error')
                while temp != password:
                    password = input('password : ')
                    temp = input('Repeat password : ')

        Customer(first_name, last_name, username, password_hashing(password))
        logging.info(f"A Customer by username:{username} is signed up")
    else:
        print('You registered by this phone number since before!')
        logging.info(f"Try to re-register by username:{username}")


def customer_menu(costumer_username):
    print(U"\u2500" * 50)
    print(' Costumer Menu '.center(50, U"\u2500"))
    print(' ' * 20 + '1. View previous invoices')
    print(' ' * 20 + '2. Shopping')
    print(' ' * 20 + '3. Back to main menu')
    print(' ' * 20 + '4. Exit')
    print(U"\u2500" * 50)
    item = input('Choose an item : ')
    if item == '1':
        Customer.view_previous_invoices(costumer_username)
        customer_menu(costumer_username)
    elif item == '2':
        shopping(costumer_username)
        customer_menu(costumer_username)
    elif item == '3':
        main_menu()
    elif item == '4':
        sys.exit()
    else:
        customer_menu(costumer_username)


def shopping(costumer_username_):
    def shopping_menu2(costumer_username, market_name):
        print(U"\u2500" * 50)
        print(f"Your chosen Market : {market_name}")
        print(' ' * 20 + '1. View list of products')
        print(' ' * 20 + '2. Product search')
        print(' ' * 20 + '3. Add a Product to cart')
        print(' ' * 20 + '4. View pre_invoice')
        print(' ' * 20 + '5. Back')
        print(' ' * 20 + '6. Exit')
        print(U"\u2500" * 50)
        item = input('choose an item: ')
        if item == '1':
            Market.view_list_of_products(market_name)
            shopping_menu2(costumer_username, market_name)
        elif item == '2':
            product_name = input('Enter the name of product : ')
            product_brand = input('Enter the brand of product : ')
            Market.find_product_by_name_and_brand(market_name, product_name, product_brand)
            shopping_menu2(costumer_username, market_name)
        elif item == '3':
            product_name = input('Enter the name of product : ')
            product_brand = input('Enter the brand : ')
            count = input(f'How many {product_name}s do you want? ')
            factored_product = Market.check_inventory(market_name, product_name, product_brand, count)
            if factored_product:
                Customer.insert_to_cart(costumer_username, market_name, factored_product)
            shopping_menu2(costumer_username, market_name)
        elif item == '4':
            cart = Customer.view_pre_invoice(costumer_username, market_name)
            if cart:
                print(U"\u2500" * 50)
                print(' ' * 20 + '1. Confirm purchase')
                print(' ' * 20 + '2. Edit purchase')
                print(U"\u2500" * 50)
                item = input('choose an item: ')
                if item == '1':
                    error = Market.shopping(market_name, costumer_username, cart)
                    if not error:
                        Customer.confirm_purchase(costumer_username, market_name)
                        logging.info(f"A Costumer shopped")
                    else:
                        print('Your request has been denied')
                        shopping_menu2(costumer_username, market_name)
                elif item == '2':
                    cart = Customer.view_pre_invoice(costumer_username, market_name)
                    Customer.edit_pre_invoice(costumer_username, market_name)
            else:
                print('Your cart is empty')
            shopping_menu2(costumer_username, market_name)
        elif item == '5':
            shopping(costumer_username)
        elif item == '6':
            sys.exit()

    def shopping_menu1(costumer_username):
        print(U"\u2500" * 50)
        print(' ' * 20 + '1. view all markets')
        print(' ' * 20 + '2. search a markets')
        print(' ' * 20 + '3. Select a market')
        print(' ' * 20 + '4. View previous invoice')
        print(' ' * 20 + '5. Back')
        print(' ' * 20 + '6. Exit')
        print(U"\u2500" * 50)
        item = input('choose an item: ')
        if item == '1':
            Market.view_the_list_of_active_stores()
            shopping_menu1(costumer_username)
        elif item == '2':
            string = input('Enter the name of the desired store: ')
            Market.market_search(string)
            shopping_menu1(costumer_username)
        elif item == '3':
            market_name = input('Market Name: ')
            # market_name = 'niloofar'
            result = Market.market_accurate_search(market_name, costumer_username)
            if result:
                market_name_ = result['Market Name']
                shopping_menu2(costumer_username, market_name_)
            shopping_menu1(costumer_username)
        elif item == '4':
            Customer.view_previous_invoices(costumer_username)
        elif item == '5':
            customer_menu(costumer_username)
        elif item == '6':
            sys.exit()

    shopping_menu1(costumer_username_)


if __name__ == "__main__":
    main_menu()
