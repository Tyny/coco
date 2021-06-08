#!/usr/bin/python
import sys
import csv
import locale
from string import Template
locale.setlocale(locale.LC_ALL, 'es_AR.utf8')

FIRST_PRODUCT_COLUMN = 8
TOTAL_COLUMN = -2


def parse_int(number):
    try:
        return int(number)
    except ValueError:
        return -1


def slice_products_columns(row):
    return row[FIRST_PRODUCT_COLUMN:TOTAL_COLUMN]


class Customer:
    CUSTOMER_NAME_ROW_INDEX = 3
    CUSTOMER_EMAIL_ROW_INDEX = 1

    @staticmethod
    def create_from_csv_row(csv_row):
        return Customer(csv_row)

    def __init__(self, csv_row):
        self.csv_row = csv_row

    def get_name(self):
        return self.csv_row[Customer.CUSTOMER_NAME_ROW_INDEX]

    def get_email(self):
        return self.csv_row[Customer.CUSTOMER_EMAIL_ROW_INDEX]

    def get_orders(self):
        return slice_products_columns(self.csv_row)

    def get_total(self):
        return int(self.csv_row[TOTAL_COLUMN])


class CustomerOrder:

    def __init__(self, product, qty):
        self.product = product
        self.qty = qty

    def get_qty(self):
        return self.qty

    def get_product(self):
        return self.product

    def __repr__(self):
        return self.__str__()


class CustomerOrdersFactory:

    @staticmethod
    def create_customer_order(products, customer):
        customer_orders_qty = customer.get_orders()
        orders = []

        for i, product in enumerate(products):
            order_qty = parse_int(customer_orders_qty[i])
            if order_qty > 0:
                orders.append(CustomerOrder(product, order_qty))

        return orders


class Presenter:
    def present(self):
        raise Exception("Implemented in childs")

class OrderPresenter(Presenter):
    def __init__(self, order):
        self._order = order

    def present(self):
        return f'{self._order.get_qty()} - {self._order.get_product().upper()}'


class EmailPresenter(Presenter):
    def __init__(self, email_template, customer, orders):
        self.template = email_template
        self.customer = customer
        self.customer_orders = orders

    def present(self):
        return f'Enviar a: {self.customer.get_email()}\n\n{self.present_body()}'

    def present_body(self):
        return template.substitute({'usuario': self.customer.get_name().title(), "pedidos": self._orders_table()})

    def _present_orders(self):
        return f'Este es tu pedido: \n{self._orders_table()}\n\n{self._present_total()}'

    def _orders_table(self):
        table = []
        for order in self.customer_orders:
            table.append(OrderPresenter(order).present())

        return "\n".join(table)

    def _present_total(self):
        presented_total = locale.format_string("%d", self.customer.get_total(), grouping=True)
        return f'Total: ${presented_total}'


if __name__ == '__main__':


    csv_file = sys.argv[1]
    template_file = sys.argv[2]
    template = None

    with open(f'./template.txt', 'r') as template_file:
        template = Template(template_file.read())


    with open(f'./{csv_file}', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        products = slice_products_columns(next(reader))

        presenters = []
        for customer_row in reader:
            customer = Customer.create_from_csv_row(customer_row)
            if not customer.get_email():
                continue

            orders = CustomerOrdersFactory.create_customer_order(products, customer)
            presenters.append(EmailPresenter(template, customer, orders))

        for presenter in presenters:
            print("----------------------------------------------------------------------")
            print(presenter.present())

