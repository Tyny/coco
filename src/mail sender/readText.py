# Prompt for txt name
# text_name = input("Ingresa el nombre del archivo con .txt: ")

# Make a list with all orders, separating mail and order
def get_orders(text_name):
    with open(text_name, "r") as file:
        # aux_list has mail in first position and order in second position
        aux_list = []

        # orders has all clients orders in lists like aux_list
        orders = []
        order = ""

        for line in file:
            # Find order separator
            if line.rstrip() != 51 * "-" :
                if line.find("Enviar a:") != -1:
                    mail = line.split(": ")
                    aux_list.append(mail[1])
                else:
                    order += line
            elif line.rstrip() == 51 * "-":
                aux_list.append(order)
                orders.append(aux_list)
                # Re-initiate aux-list and order
                aux_list = []
                order = ""
        return orders


def get_number_of_clients(text_name):
    with open(text_name, "r") as file:
        clients = 0;
        for line in file:
            if line.rstrip() == 51 * "-":
                clients +=1 
        return clients




# orders = get_orders(text_name)
# print(orders[1][0])
# print(orders[1][1])
