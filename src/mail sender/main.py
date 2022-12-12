from lib2to3.pgen2.pgen import DFAState
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter.filedialog import askopenfile
from readText import get_orders
from mail_compras import send_email, check_sended_mails, send_email_template
import re
import time
import datetime


# Define variable to upload txt file with all orders and to save file path
orders = []
file_path = ""

# Get current time
current_time = datetime.datetime.now()
months = {1:"Enero", 2: "Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10: "Octubre", 11:"Noviembre", 12:"Diciembre"}
month = months[current_time.month]


# Open text file to send mail
def open_file():
    global orders
    global file_path
    file_path = askopenfile(mode='r', filetypes=[("Text Files", "*.txt")])
    orders = get_orders(file_path.name)
    if len(orders) > 0:
        messagebox.showinfo("Archivo Cargado", "Se cargaron " + str(len(orders)) + " pedidos del archivo " + file_path.name.split("/")[-1])


# Send mail with orders
def MandarMail():
    global orders
    global file_path
    try:
        confirmacion = messagebox.askyesno("Más vale prevenir que curar", 
                                            "Vas a usar el archivo " 
                                            + file_path.name.split("/")[-1]
                                            + " con " + str(len(orders)) 
                                            + " pedidos para mandar mail.\n ¿Está ok?")
        if confirmacion:
            for i in range(len(orders)):
                send_email(orders[i][1], orders[i][0])
            
            info_mails = check_sended_mails()
            rebotados = info_mails["hardBounces"] + info_mails["softBounces"]
            messagebox.showinfo("Info de mails", 
                                "En las últimas 24 hs salieron " + str(info_mails["requests"]) + " mails.\n" 
                                + str(info_mails["delivered"]) + " se enviaron correctamente. \n"
                                + str(rebotados) + " fueron rebotados. \n"
                                + str(info_mails["spamReports"]) + " fueron a Spam. \n"
                                + str(info_mails["blocked"]) + " fueron bloqueados." )
    except AttributeError:
                messagebox.showerror("Ups!Algo anda mal...", "Faltó cargar el archivo.")
    except IndexError:
                messagebox.showerror("Ups!Algo anda mal...", "Parece que el archivo que elegiste no tiene pedidos.")


def focus_mail_prueba_entry(_):
    entry_mail_prueba.delete(0, END)
    entry_mail_prueba.config(foreground='black')


def MandarMailPrueba():
    global orders
    global file_path
    try:
        mail_prueba = var_mail_prueba.get()
        re_mail = "^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
        if re.search(re_mail, mail_prueba):
            send_email("Primer Pedido: \n" 
                        + orders[0][1] + 51 * "-" + "\n"
                        + " \n Último Pedido: \n"
                        + orders[-1][1]
                        , mail_prueba)
        else:
            messagebox.showerror("Ups!Algo anda mal...", "El mail ingresado no es válido.")
    except AttributeError:
        messagebox.showerror("Ups!Algo anda mal...", "Faltó cargar el archivo.")
    except IndexError:
        messagebox.showerror("Ups!Algo anda mal...", "Parece que el archivo que elegiste no tiene pedidos.")

app = Tk() 
app.title('Mails Correntosa')
app.geometry('450x150') 

var_mail_prueba = StringVar()    

subarch = Label(
    app, 
    text="Subir archivo de texto con pedidos" #agregar mes menos 1 automáticamente? 
    )
subarch.grid(row=1, column=0, padx=10)

subarchbtn = Button(
    app, 
    text ='Subir Archivo', 
    command = open_file
    ) 
subarchbtn.grid(row=1, column=1)

mailPrueba = Button(
    app, text = "Mandar Mail de Prueba",
    command = MandarMailPrueba
)
mailPrueba.grid(row = 2, column = 1, pady = 10)

upld = Button(
    app, 
    text='Mandar Mails', 
    command= MandarMail
    )
upld.grid(row = 3, column = 1, pady = 10)
entry_mail_prueba = Entry(app, textvariable = var_mail_prueba, width = 20, foreground = "grey")
entry_mail_prueba.grid(row = 2,column = 0)
entry_mail_prueba.insert(0, "Escribir Mail")

entry_mail_prueba.bind("<FocusIn>", focus_mail_prueba_entry)
app.mainloop()