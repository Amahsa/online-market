import datetime


class Invoice:
    def __init__(self, market_name, costumer_phone, products):
        self.market_name = market_name
        self.costumer_phone = costumer_phone
        self.products = products
        self.total_price = self.set_total_price()
        self.date = str(datetime.datetime.now())

    def set_total_price(self):
        total_price = 0
        for item in self.products:
            total_price += int(item['price'])
        return total_price
