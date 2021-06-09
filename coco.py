#!/usr/bin/python3
import sys
import csv
import locale
from string import Template, ascii_letters
locale.setlocale(locale.LC_ALL, 'es_AR.utf8')

FIRST_PRODUCT_COLUMN = 9
LAST_PRODUCT_COLUMN = 131
TOTAL_COLUMN = 132

CUSTOMER_NAME_ROW_INDEX = 4
CUSTOMER_EMAIL_ROW_INDEX = 2


def parse_int(number):
    try:
        return int(number)
    except ValueError:
        return -1


def slice_products_columns(row):
    return row[FIRST_PRODUCT_COLUMN - 1:LAST_PRODUCT_COLUMN]


def column_to_number(col):
    num = 0
    for c in col:
        if c in ascii_letters:
            num = num * 26 + (ord(c.upper()) - ord('A')) + 1
    return num


def number_to_column(n):
    name = ''
    while n > 0:
        n, r = divmod(n - 1, 26)
        name = chr(r + ord('A')) + name
    return name


class Customer:
    @staticmethod
    def create_from_csv_row(csv_row):
        return Customer(csv_row)

    def __init__(self, csv_row):
        self.csv_row = csv_row

    def get_name(self):
        return self.csv_row[CUSTOMER_NAME_ROW_INDEX - 1]

    def get_email(self):
        return self.csv_row[CUSTOMER_EMAIL_ROW_INDEX - 1]

    def get_orders(self):
        return slice_products_columns(self.csv_row)

    def get_total(self):
        return int(self.csv_row[TOTAL_COLUMN - 1])


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
        return template.substitute({
            'usuario': self.customer.get_name().title(),
            "pedidos": self._orders_table(),
            "total": self._present_total()}
        )

    def _orders_table(self):
        table = []
        for order in self.customer_orders:
            table.append(OrderPresenter(order).present())

        return "\n".join(table)

    def _present_total(self):
        presented_total = locale.format_string("%d", self.customer.get_total(), grouping=True)
        return f'${presented_total}'

class ScriptConfiguration():
    @staticmethod
    def configure_script():
        global CUSTOMER_NAME_ROW_INDEX
        global CUSTOMER_EMAIL_ROW_INDEX
        global FIRST_PRODUCT_COLUMN
        global LAST_PRODUCT_COLUMN
        global TOTAL_COLUMN

        csv_file = sys.argv[1]
        template_file = sys.argv[2]
        output_file = sys.argv[3]

        customer_email_row_index = input(f'Ingresa la columna donde esta el email del consumidor (valor actual es {number_to_column(CUSTOMER_EMAIL_ROW_INDEX)}): ')
        customer_email_row_index = customer_email_row_index.strip().lower()
        if len(customer_email_row_index) > 0:
            CUSTOMER_EMAIL_ROW_INDEX = column_to_number(customer_email_row_index)

        customer_name_row_index = input(f'Ingresa la columna donde esta el nombre del consumidor (valor actual es {number_to_column(CUSTOMER_NAME_ROW_INDEX)}): ')
        customer_name_row_index = customer_name_row_index.strip().lower()
        if len(customer_name_row_index) > 0:
            CUSTOMER_NAME_ROW_INDEX = column_to_number(customer_name_row_index)

        first_product_column = input(f'Ingresa la primera columna de productos (valor actual es {number_to_column(FIRST_PRODUCT_COLUMN)}): ')
        first_product_column.strip().lower()
        if len(first_product_column) > 0:
            FIRST_PRODUCT_COLUMN = column_to_number(first_product_column)

        last_product_column = input(f'Ingresa la ultima columna de productos (valor actual es {number_to_column(LAST_PRODUCT_COLUMN)}): ')
        last_product_column = last_product_column.strip().lower()
        if len(last_product_column) > 0:
            LAST_PRODUCT_COLUMN = column_to_number(last_product_column)

        total_column = input(f'Ingresa la columna de totales (valor actual es {number_to_column(TOTAL_COLUMN)}): ')
        total_column = total_column.strip().lower()
        if len(total_column) > 0:
            TOTAL_COLUMN = column_to_number(total_column)

        print("\n\n")
        print("Configuration actual:")
        print("-------------------------------------------------------------------------------------------")
        print("CUSTOMER_EMAIL_ROW_INDEX", number_to_column(CUSTOMER_EMAIL_ROW_INDEX))
        print("CUSTOMER_NAME_ROW_INDEX", number_to_column(CUSTOMER_NAME_ROW_INDEX))
        print("FIRST_PRODUCT_COLUMN", number_to_column(FIRST_PRODUCT_COLUMN))
        print("LAST_PRODUCT_COLUMN", number_to_column(LAST_PRODUCT_COLUMN))
        print("TOTAL_COLUMN", number_to_column(TOTAL_COLUMN))
        print("-------------------------------------------------------------------------------------------")

        return csv_file, template_file, output_file

if __name__ == '__main__':
    csv_file, template_file, output_file = ScriptConfiguration.configure_script()

    template = None
    with open(f'{template_file}', 'r') as template_file:
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

        with open(f'coco.{output_file}', 'w') as output:
            for presenter in presenters:
                output.write(presenter.present())
                output.write("---------------------------------------------------")
                output.write("\n\n")

    print(f'Encontra el resultado en {output_file}! :)')

