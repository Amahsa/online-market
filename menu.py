import logging
from market import Market
from All_Users_File_Handler import UsersFileHandler
import sys
import hashlib

logging.basicConfig(level=logging.DEBUG, filename='Log.log', filemode='a',
                    format='%(asctime)s - %(process)d - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


def password_hashing(password):
    hashed_password = hashlib.sha256(password.encode())
    return hashed_password.hexdigest()


def user_not_taken(username):
    all_users_file = UsersFileHandler()
    all_users = all_users_file.read_file()
    found = False
    for item in all_users:
        if item['username'] == username:
            found = True
            break
    if not found:
        return True


def user_info(username):
    all_users = UsersFileHandler()
    for item in all_users.read_file():
        if item['username'] == username:
            return item


def add_product(username):
    # print('market, product_name, brand, product_count, product_price, barcode, expiration_date')
    item = 'y'
    while item == 'y':
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
        item = input('continue to add product (y/n)? ').lower()


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


def register():
    print(' ' * 20 + '1. Market manager')
    print(' ' * 20 + '2. Customer')
    print(' ' * 20 + '3. Exit')
    item = input('Chose an item: ')
    if item == '1':
        username = input('Phone number (this will e your username): ')
        if user_not_taken(username):
            password = input('Password : ')
            temp = input('Repeat password : ')
            if temp != password:
                print('Error')
                while temp != password:
                    password = input('password : ')
                    temp = input('Repeat password : ')
            market_name = input('Market name : ')
            start_working = input('Opening time (Use 24-hour format): ')
            end_working = input('Closing time (Use 24-hour format): ')
            if float(end_working) <= float(start_working):
                print('Closing time most be grater than opening time ')
                while float(end_working) <= float(start_working):
                    start_working = input('Opening time (Use 24-hour format): ')
                    end_working = input('Closing time (Use 24-hour format): ')
            Market(username, password_hashing(password), market_name, start_working, end_working)
            logging.info(f"A manager by username:{username} is signed up")
        else:
            print('This username is taken by someone else!')
            logging.info(f"Try to re-register by username:{username}")
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
                custemer_menu(user['username'])
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
    else:
        print('No user found! please sign up or check the username')
        logging.warning(f"Try to sign in with unavailable  username:{username}")
    main_menu()


def market_manager_menu(username):
    print(' Manager Menu '.center(50,U"\u2500"))
    print(' ' * 20 + '1. Register product list')
    print(' ' * 20 + '2. Product inventory')
    print(' ' * 20 + '3. Unavailable products')
    print(' ' * 20 + '4. Customers purchase invoices')
    print(' ' * 20 + '5. Invoice search')
    print(' ' * 20 + '6. Show all costumers')
    print(' ' * 20 + '7. Block a costumer')
    print(' ' * 20 + '8. Exit')
    print(U"\u2500" * 50)
    item = input('Chose an item: ')
    if item == '1':
        add_product(username)
    elif item == '2':
        Market.inventory(username)
    elif item == '3':
        Market.inventory_alert(username)
    elif item == '4':
        Market.customer_purchase_invoices(username)
    elif item == '5':
        Market.invoice_search(username)
    elif item == '6':
        Market.customer_list(username)
    elif item == '7':
        customer_exist = Market.customer_list(username)
        if customer_exist:
            costumer = input('Which costumer do you want to block? (Enter Username)')
            Market.block_customer(username, costumer)
    elif item == '8':
        sys.exit()
    market_manager_menu(username)


def custemer_menu(username):
    print('1. ')


main_menu()
