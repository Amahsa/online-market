import logging
from market import Market
from All_Users_File_Handler import UsersFileHandler
import sys
import hashlib
import re
from datetime import time

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
    found = False
    if all_users:
        for item in all_users:
            if item['username'] == username:
                found = True
                return False
        if not found:
            return True
    return True


def user_info(username):
    all_users = UsersFileHandler()
    for item in all_users.read_file():
        if item['username'] == username:
            return item


def add_product(username):
    # print('market, product_name, brand, product_count, product_price, barcode, expiration_date')
    continue_ = 'y'
    while continue_ == 'y':
        product_name = input('product name : ')
        brand = input('brand : ')
        product_count = input('count : ')
        product_price = input('price : ')
        barcode = input('barcode : ')
        expiration_date = input('expiration date (dd-mm-yyyy): ')
        Market.register_product_list(username=username, product_name=product_name, brand=brand,
                                     product_count=product_count, product_price=product_price, barcode=barcode,
                                     expiration_date=expiration_date)
        logging.info(f"A market manager by username:{username} added a product")
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
            start_working = list(map(int, start_working.split(':')))
            start_working = time(start_working[0], start_working[1], start_working[2])
            while not validation_time(str(end_working)):
                end_working = input('Closing time (Use 24-hour format hh:mm:ss): ')
            end_working = list(map(int, end_working.split(':')))
            end_working = time(end_working[0], end_working[1], end_working[2])
            # if end_working < start_working:
            #     while end_working <= start_working:
            #         print('Enter valid time ')
            #         start_working = input('Opening time (Use 24-hour format): ')
            #         end_working = input('Closing time (Use 24-hour format): ')
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
    if item == '2':
        pass
    else:
        sys.exit()


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
                    Market.inventory_alert(username)
                except Exception as e:
                    logging.exception('error in showing inventory', exc_info=True)
                logging.info(f"A manager by username:{user['username']} signed in")
                market_manager_menu(user['username'])
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
    print(' ' * 20 + '1. Register product list')
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
        Market.view_inventory(username)
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


def customer_menu(username):
    print('1. ')


main_menu()
