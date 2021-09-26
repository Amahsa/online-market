from prettytable import PrettyTable
from prettytable import from_csv
x = PrettyTable()


x.field_names = ['X','Y']
x.add_row(['dddddddddddd','rr'])
x.add_row(['','yyyyyyyyyyy'])

print(x)

with open('AllMarkets.txt') as f:
    my_table = from_csv(f)

print(my_table)

x.field_names = ['X','Y']
x.add_row(['dddddddddddd','rr'])
x.add_row([my_table,'yyyyyyyyyyy'])

print(x)