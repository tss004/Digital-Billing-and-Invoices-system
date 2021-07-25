from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tmsg
import os
import time
import smtplib as sm
import tkinter.font as font
menu_category = ["Dairy","Household"]

menu_category_dict = {"Dairy":"1 Dairy.txt","Household":"2 Household.txt"}

order_dict = {}
for i in menu_category:
    order_dict[i] = {}
cwd = os.getcwd()
def load_menu():
    menuCategory.set("")
    menu_tabel.delete(*menu_tabel.get_children())
    menu_file_list = os.listdir("Menu")
    for file in menu_file_list:
        f = open("Menu\\" + file , "r")
        category=""
        while True:
            line = f.readline()
            if(line==""):
                menu_tabel.insert('',END,values=["","",""])
                break
            elif (line=="\n"):
                continue
            elif(line[0]=='#'):
                category = line[1:-1]
                name = "\t\t"+line[:-1]
                price = ""
            elif(line[0]=='*'):
                name = line[:-1]
                price = ""
            else:
                name = line[:line.rfind(" ")]
                price = line[line.rfind(" ")+1:-3]
            
            menu_tabel.insert('',END,values=[name,price,category])
        

def load_order():
    order_tabel.delete(*order_tabel.get_children())
    for category in order_dict.keys():
        if order_dict[category]:
            for lis in order_dict[category].values():
                order_tabel.insert('',END,values=lis)
    update_total_price()

def add_button_operation():
    name = itemName.get()
    rate = itemRate.get()
    category = itemCategory.get()
    quantity = itemQuantity.get()

    if name in order_dict[category].keys():
        tmsg.showinfo("Error", "Item already exist in your order")
        return
    if not quantity.isdigit():
        tmsg.showinfo("Error", "Please Enter Valid Quantity")
        return
    lis = [name,rate,quantity,str(int(rate)*int(quantity)),category]
    order_dict[category][name] = lis
    load_order()
    
def load_item_from_menu(event):
    cursor_row = menu_tabel.focus()
    contents = menu_tabel.item(cursor_row)
    row = contents["values"]

    itemName.set(row[0])
    itemRate.set(row[1])
    itemCategory.set(row[2])
    itemQuantity.set("1")

def load_item_from_order(event):
    cursor_row = order_tabel.focus()
    contents = order_tabel.item(cursor_row)
    row = contents["values"]

    itemName.set(row[0])
    itemRate.set(row[1])
    itemQuantity.set(row[2])
    itemCategory.set(row[4])

def show_button_operation():
    category = menuCategory.get()
    if category not in menu_category:
        tmsg.showinfo("Error", "Please select valid Choice")
    else:
        menu_tabel.delete(*menu_tabel.get_children())
        f = open("Menu\\" + menu_category_dict[category] , "r")
        while True:
            line = f.readline()
            if(line==""):
                break
            if (line[0]=='#' or line=="\n"):
                continue
            if(line[0]=='*'):
                name = "\t"+line[:-1]
                menu_tabel.insert('',END,values=[name,"",""])
            else:
                name = line[:line.rfind(" ")]
                price = line[line.rfind(" ")+1:-3]
                menu_tabel.insert('',END,values=[name,price,category])

def clear_button_operation():
    itemName.set("")
    itemRate.set("")
    itemQuantity.set("")
    itemCategory.set("")
    customerName.set("")
    customerContact.set("")
    customeremail.set("")

def cancel_button_operation():
    names = []
    for i in menu_category:
        names.extend(list(order_dict[i].keys()))
    if len(names)==0:
        tmsg.showinfo("Error", "Your order list is Empty")
        return
    ans = tmsg.askquestion("Cancel Order", "Are You Sure to Cancel Order?")
    if ans=="no":
        return
    order_tabel.delete(*order_tabel.get_children())
    for i in menu_category:
        order_dict[i] = {}
    clear_button_operation()
    update_total_price()

def update_button_operation():
    name = itemName.get()
    rate = itemRate.get()
    category = itemCategory.get()
    quantity = itemQuantity.get()

    if category=="":
        return
    if name not in order_dict[category].keys():
        tmsg.showinfo("Error", "Item is not in your order list")
        return
    if order_dict[category][name][2]==quantity:
        tmsg.showinfo("Error", "No changes in Quantity")
        return
    order_dict[category][name][2] = quantity
    order_dict[category][name][3] = str(int(rate)*int(quantity))
    load_order()

def remove_button_operation():
    name = itemName.get()
    category = itemCategory.get()

    if category=="":
        return
    if name not in order_dict[category].keys():
        tmsg.showinfo("Error", "Item is not in your order list")
        return
    del order_dict[category][name]
    load_order()

def update_total_price():
    price = 0
    for i in menu_category:
        for j in order_dict[i].keys():
            price += int(order_dict[i][j][3])
    if price == 0:
        totalPrice.set("")
    else:
        totalPrice.set("Rs. "+str(price)+"  /-")

def bill_button_operation():
    customer_name = customerName.get()
    customer_contact = customerContact.get()
    customer_email = customeremail.get()
    names = []
    for i in menu_category:
        names.extend(list(order_dict[i].keys()))
    if len(names)==0:
        tmsg.showinfo("Error", "Your order list is Empty")
        return
    if customer_name=="" or customer_contact=="":
        tmsg.showinfo("Error", "Customer Details Required")
        return
    if not customerContact.get().isdigit():
        tmsg.showinfo("Error", "Invalid Customer Contact")
        return   
    #ans = tmsg.askquestion("Generate Bill", "Are You Sure to Generate Bill?")
    ans = "yes"
    if ans=="yes":
        bill = Toplevel()
        bill.title("Bill")
        bill.geometry("670x500+300+100")
        bill_text_area = Text(bill, font=("times new roman", 12))
        st = "\tINDIAN INSTITUTE OF INFORMATION TECHNOLOGY NAGPUR (IIITN)\n\t\t\tSEMINARY HILLS, NAGPUR\n"
        ts= "INDIAN INSTITUTE OF INFORMATION TECHNOLOGY, NAGPUR\n\t\t\n"
        ts+= "-"*70 + "BILL" + "-"*36 + "\nDate:- "
        st += "-"*61 + "BILL" + "-"*61 + "\nDate:- "

        
        t = time.localtime(time.time())
        week_day_dict = {0:"Monday",1:"Tuesday",2:"Wednesday",3:"Thursday",4:"Friday",5:"Saturday",  6:"Sunday"}

        st += f"{t.tm_mday} / {t.tm_mon} / {t.tm_year} ({week_day_dict[t.tm_wday]})"
        ts+= f"{t.tm_mday} / {t.tm_mon} / {t.tm_year} ({week_day_dict[t.tm_wday]})"
        ts+= " "*10 + f"\nTime:- {t.tm_hour} : {t.tm_min} : {t.tm_sec}"
        st += " "*10 + f"\t\t\t\t\t\tTime:- {t.tm_hour} : {t.tm_min} : {t.tm_sec}"

        
        st += f"\nCustomer Name:- {customer_name}\nCustomer Contact:- {customer_contact}\nCustomer email:- {customer_email}\n"
        ts+= f"\nCustomer Name:- {customer_name}\nCustomer Contact:- {customer_contact}\nCustomer email:- {customer_email}\n"
        ts+= "-"*110 + "\n"  + "Product name\t\tQuantity\tAmount\n"
        st += "-"*130 + "\n" + " "*4 + "DESCRIPTION\t\t\t\t\tRATE\tQUANTITY\t\tAMOUNT\n"
        ts+= "-"*111 + "\n"
        st += "-"*130 + "\n"

        
        for i in menu_category:
            for j in order_dict[i].keys():
                lis = order_dict[i][j]
                name = lis[0]
                rate = lis[1]
                quantity = lis[2]
                price = lis[3]
                st += name + "\t\t\t\t\t" + rate + "\t      " + quantity + "\t\t  " + price + "\n\n"
                ts+= name + "\t\t\t"  + quantity + "\t " + price + "\n\n"
        ts+="-"*111
        st += "-"*130

        ts+=f"\n\t\t\tTotal price : {totalPrice.get()}\n"
        st += f"\n\t\t\tTotal price : {totalPrice.get()}\n"
        st += "-"*130

        
        bill_text_area.insert(1.0, st)
        
        folder = f"{t.tm_mday}-{t.tm_mon}-{t.tm_year}"
        if not os.path.exists(f"Bill Records\\{folder}"):
            os.makedirs(f"Bill Records\\{folder}")
        file = open(f"Bill Records\\{folder}\\{customer_name+customer_contact}.txt", "w")
        file.write(st)
        file.close()
        if not os.path.exists(f"All Bill Records"):
            os.makedirs(f"All Bill Records")
        file = open(f"All Bill Records\\{customer_name+customer_contact}.txt", "w")
        file.write(st)
        file.close()
        server=sm.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login("@gmail.com","password")
        subject="Digital Invoice from my shop"
        body=ts
        message="Subject:{}\n\n{}".format(subject,body)
        server.sendmail("@gmail.com",customer_email,message)
        server.quit()
        
        order_tabel.delete(*order_tabel.get_children())
        for i in menu_category:
            order_dict[i] = {}
        clear_button_operation()
        update_total_price()
        customerName.set("")
        customerContact.set("")
        customeremail.set("")
        bill_text_area.pack(expand=True, fill=BOTH)
        bill.focus_set()

def close_window():
    tmsg.showinfo("Thanks", "Thanks for using our service")
    root.destroy()
def Unpaid():
    customer_name = customerName.get()
    customer_contact = customerContact.get()
    customer_email = customeremail.get()
    bill = Toplevel()
    bill.title("Bill")
    bill.geometry("670x500+300+100")
    bill_text_area = Text(bill, font=("times new roman", 12))
    st = "\tINDIAN INSTITUTE OF INFORMATION TECHNOLOGY NAGPUR (IIITN)\n\t\t\tSEMINARY HILLS, NAGPUR\n"
    ts= "INDIAN INSTITUTE OF INFORMATION TECHNOLOGY, NAGPUR\n\t\t\n"
    ts+= "-"*70 + "BILL" + "-"*36 + "\nDate:- "
    st += "-"*61 + "BILL" + "-"*61 + "\nDate:- "

    
    t = time.localtime(time.time())
    week_day_dict = {0:"Monday",1:"Tuesday",2:"Wednesday",3:"Thursday",4:"Friday",5:"Saturday",  6:"Sunday"}

    st += f"{t.tm_mday} / {t.tm_mon} / {t.tm_year} ({week_day_dict[t.tm_wday]})"
    ts+= f"{t.tm_mday} / {t.tm_mon} / {t.tm_year} ({week_day_dict[t.tm_wday]})"
    ts+= " "*10 + f"\nTime:- {t.tm_hour} : {t.tm_min} : {t.tm_sec}"
    st += " "*10 + f"\t\t\t\t\t\tTime:- {t.tm_hour} : {t.tm_min} : {t.tm_sec}"

    
    st += f"\nCustomer Name:- {customer_name}\nCustomer Contact:- {customer_contact}\nCustomer email:- {customer_email}\n"
    ts+= f"\nCustomer Name:- {customer_name}\nCustomer Contact:- {customer_contact}\nCustomer email:- {customer_email}\n"
    ts+= "-"*110 + "\n"  + "Product name\t\tQuantity\tAmount\n"
    st += "-"*130 + "\n" + " "*4 + "DESCRIPTION\t\t\t\t\tRATE\tQUANTITY\t\tAMOUNT\n"
    ts+= "-"*111 + "\n"
    st += "-"*130 + "\n"

    
    for i in menu_category:
        for j in order_dict[i].keys():
            lis = order_dict[i][j]
            name = lis[0]
            rate = lis[1]
            quantity = lis[2]
            price = lis[3]
            st += name + "\t\t\t\t\t" + rate + "\t      " + quantity + "\t\t  " + price + "\n\n"
            ts+= name + "\t\t\t"  + quantity + "\t " + price + "\n\n"
    ts+="-"*111
    st += "-"*130

    ts+=f"\n\t\t\tTotal price : {totalPrice.get()}\n"
    st += f"\n\t\t\tTotal price : {totalPrice.get()}\n"
    st += "-"*130

    
    bill_text_area.insert(1.0, st)
    if not os.path.exists('Unpaid Bills'):
        os.makedirs('Unpaid Bills')
    file=open(f"Unpaid Bills\\{customer_name+customer_contact}.txt","w")
    file.write(st) 
    file.close()
    if not os.path.exists(f"All Bill Records"):
        os.makedirs(f"All Bill Records")
    file = open(f"All Bill Records\\{customer_name+customer_contact}.txt", "w")
    file.write(st)
    file.close()
    server=sm.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login("@gmail.com","password")
    subject="Digital Invoice from my shop"
    body=ts
    message="Subject:{}\n\n{}".format(subject,body)
    server.sendmail("@gmail.com",customer_email,message)
    server.quit()

    
        
    #tmsg.showinfo(" ","Added to Unpaid Folder")
    
    
    order_tabel.delete(*order_tabel.get_children())
    for i in menu_category:
        order_dict[i] = {}
    clear_button_operation()
    update_total_price()
    customerName.set("")
    customerContact.set("")
    customeremail.set("")

    bill_text_area.pack(expand=True, fill=BOTH)
    bill.focus_set()




def additemtoDB():
    stri=f"\n{ItemNamea.get()} {Itempricea.get()}/-"
    i=""
    if menuCategorya.get()=="Dairy":
        fz = open("Menu/1 "+menuCategorya.get()+".txt", "a")
        fz.write(stri)
        fz.close()
    elif menuCategorya.get()=="Household":
        fz = open("Menu/2 "+menuCategorya.get()+".txt", "a")
        fz.write(stri)
        fz.close()
    ItemNamea.set("")
    menuCategorya.set("")
    Itempricea.set("")
    
    
def removeitemtoDB():
    strin=f"{ItemNameup.get()} {Itempriceup.get()}/-"
    if menuCategoryb.get()=="Dairy":
        with open("Menu/1 "+menuCategoryb.get()+".txt", "r") as fa:

            linesz = fa.readlines()

        with open("Menu/1 "+menuCategoryb.get()+".txt", "w") as fa:

            for linea in linesz:

                if linea.strip("\n") != strin:

                    fa.write(linea)
    elif menuCategoryb.get()=="Household":
        with open("Menu/2 "+menuCategoryb.get()+".txt", "r") as fa:

            linesz = fa.readlines()

        with open("Menu/2 "+menuCategoryb.get()+".txt", "w") as fa:

            for linea in linesz:

                if linea.strip("\n") != strin:

                    fa.write(linea)
    ItemNameup.set("")
    Itempriceup.set("")
    menuCategoryb.set("")
def Findbill():
    zi=findbill.get()
    findbill.set("")
    y="All Bill Records/"+zi+".txt"
    with open(y,'r') as file:
        countriesStr = file.read()
    root = Tk()
    

    root.geometry("670x500+300+100")
    
    T = Text(root, height = 500, width = 500)

    T.pack()

    

    T.insert( END,countriesStr)
    
    ttk.mainloop()
    findbill.set('')

root = Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("Welcome to Apni Dukan")


style_button = ttk.Style()
style_button.configure("TButton",font = ("times new roman",10,"bold"),
   background="lightgreen")

title_frame = Frame(root, bd=8, bg="#696969", relief=GROOVE)
title_frame.pack(side=TOP, fill="x")

title_label = Label(title_frame, text="Apni Dukan",relief=GROOVE ,
                    font=("times new roman", 20, "bold"),bg = "#696969", fg="white", pady=5)
title_label.pack()






customer_frame = LabelFrame(root,text="Customer Details",font=("times new roman", 15, "bold"),bd=8, bg="#696969",fg="white", relief=GROOVE)
customer_frame.pack(side=TOP, fill="x")


customer_name_label = Label(customer_frame, text="Name", font=("times new roman", 15, "bold"),bg = "#696969", fg="white")
customer_name_label.grid(row = 0, column = 0)

customerName = StringVar()
customerName.set("")
customer_name_entry = Entry(customer_frame,width=10,font="arial 15",bd=5,textvariable=customerName)
customer_name_entry.grid(row =0 , column=1,padx=50)


customer_contact_label = Label(customer_frame, text="Contact", 
                    font=("times new roman", 15, "bold"),bg = "#696969", fg="white")
customer_contact_label.grid(row = 0, column = 2)

customerContact = StringVar()
customerContact.set("")
customer_contact_entry = Entry(customer_frame,width=10,font="arial 15",bd=5,
                                textvariable=customerContact)
customer_contact_entry.grid(row = 0, column=3,padx=50)


customer_email_label = Label(customer_frame, text="Email", 
                    font=("times new roman", 15, "bold"),bg = "#696969", fg="white")
customer_email_label.grid(row = 0, column = 4)

customeremail = StringVar()
customeremail.set("")
customer_email_entry = Entry(customer_frame,width=23,font="arial 15",bd=5,
                                textvariable=customeremail)
customer_email_entry.grid(row = 0, column=5,padx=50)

customer_email_label = Label(customer_frame, text="BillName", 
                    font=("times new roman", 15, "bold"),bg = "#696969", fg="white")
customer_email_label.grid(row = 0, column = 6)
findbill = StringVar()
findbill.set("")
customer_email_entry = Entry(customer_frame,width=15,font="arial 15",bd=5,
                                textvariable=findbill)
customer_email_entry.grid(row = 0, column=7,padx=5)

cancel_button = ttk.Button(customer_frame,
                         text="Find Bill",command=Findbill)
cancel_button.grid(row = 0, column=8,padx=5,ipadx=10,ipady=8)



menu_frame = Frame(root,bd=8, bg="#696969", relief=GROOVE)
menu_frame.place(x=0,y=125,height=490,width=650)

menu_label = Label(menu_frame, text="Menu", 
                    font=("times new roman", 20, "bold"),bg = "#696969", fg="white", pady=0)
menu_label.pack(side=TOP,fill="x")

menu_category_frame = Frame(menu_frame,bg="#696969",pady=10)
menu_category_frame.pack(fill="x")

combo_lable = Label(menu_category_frame,text="Select Type", 
                    font=("times new roman", 12, "bold"),bg = "#696969", fg="white")
combo_lable.grid(row=0,column=0,padx=10)

menuCategory = StringVar()
combo_menu = ttk.Combobox(menu_category_frame,values=menu_category,
                            textvariable=menuCategory)
combo_menu.grid(row=0,column=1,padx=30,ipadx=5,ipady=5)

show_button = ttk.Button(menu_category_frame, text="Show",width=8,
                        command=show_button_operation,)
show_button.grid(row=0,column=4,padx=60,ipadx=10,ipady=10)

show_all_button = ttk.Button(menu_category_frame, text="Show All",
                        width=8,command=load_menu)
show_all_button.grid(row=0,column=5,ipadx=10,ipady=10)

menu_tabel_frame = Frame(menu_frame)
menu_tabel_frame.pack(fill=BOTH,expand=1)

scrollbar_menu_x = Scrollbar(menu_tabel_frame,orient=HORIZONTAL)
scrollbar_menu_y = Scrollbar(menu_tabel_frame,orient=VERTICAL)

style = ttk.Style()
style.configure("Treeview.Heading",font=("times new roman",13, "bold"))
style.configure("Treeview",font=("times new roman",12),rowheight=25)

menu_tabel = ttk.Treeview(menu_tabel_frame,style = "Treeview",columns =("name","price","category"),xscrollcommand=scrollbar_menu_x.set,yscrollcommand=scrollbar_menu_y.set)

menu_tabel.heading("name",text="Name")
menu_tabel.heading("price",text="Price")
menu_tabel["displaycolumns"]=("name", "price")
menu_tabel["show"] = "headings"
menu_tabel.column("price",width=50,anchor='center')

scrollbar_menu_x.pack(side=BOTTOM,fill=X)
scrollbar_menu_y.pack(side=RIGHT,fill=Y)

scrollbar_menu_x.configure(command=menu_tabel.xview)
scrollbar_menu_y.configure(command=menu_tabel.yview)

menu_tabel.pack(fill=BOTH,expand=1)

load_menu()
menu_tabel.bind("<ButtonRelease-1>",load_item_from_menu)


items_frame = Frame(root,bd=8, bg="#696969", relief=GROOVE)
items_frame.place(x=0,y=615,height=180,width=1380)

customer_name_label = Label(items_frame, text="ItemName", font=("times new roman", 15, "bold"),bg = "#696969", fg="white")
customer_name_label.grid(row = 0, column = 2)

ItemNamea = StringVar()
ItemNamea.set("")
customer_name_entry = Entry(items_frame,width=20,font="arial 15",bd=5,textvariable=ItemNamea)
customer_name_entry.grid(row =0 , column=3,padx=50)


customer_contact_label = Label(items_frame, text="setect category",  font=("times new roman", 15, "bold"),bg = "#696969", fg="white")
customer_contact_label.grid(row = 0, column = 0)

menuCategorya = StringVar()
combo_menu = ttk.Combobox(items_frame,values=menu_category, textvariable=menuCategorya)
combo_menu.grid(row=0,column=1,padx=20,ipadx=5,ipady=5)


customer_email_label = Label(items_frame, text="Price", font=("times new roman", 15, "bold"),bg = "#696969", fg="white")
customer_email_label.grid(row = 0, column = 4)

Itempricea = StringVar()
Itempricea.set("")
customer_email_entry = Entry(items_frame,width=20,font="arial 15",bd=5,
                                textvariable=Itempricea)
customer_email_entry.grid(row = 0, column=5,padx=50)

add_button = ttk.Button(items_frame, text="Add Item to DB",command=additemtoDB)
add_button.grid(row=0,column=6,padx=20,pady=30,ipadx=10,ipady=10)

#####################
customer_name_label = Label(items_frame, text="ItemName", 
                    font=("times new roman", 15, "bold"),bg = "#696969", fg="white")
customer_name_label.grid(row = 1, column = 2)

ItemNameup = StringVar()
ItemNameup.set("")
customer_name_entry = Entry(items_frame,width=20,font="arial 15",bd=5,
                                textvariable=ItemNameup)
customer_name_entry.grid(row =1 , column=3,padx=50)


customer_contact_label = Label(items_frame, text="Select category", 
                    font=("times new roman", 15, "bold"),bg = "#696969", fg="white")
customer_contact_label.grid(row = 1, column = 0)

menuCategoryb = StringVar()
combo_menu = ttk.Combobox(items_frame,values=menu_category,textvariable=menuCategoryb)
combo_menu.grid(row=1,column=1,padx=20,ipadx=5,ipady=5)


customer_email_label = Label(items_frame, text="Price", 
                    font=("times new roman", 15, "bold"),bg = "#696969", fg="white")
customer_email_label.grid(row = 1, column = 4)

Itempriceup = StringVar()
Itempriceup.set("")
customer_email_entry = Entry(items_frame,width=20,font="arial 15",bd=5,
                                textvariable=Itempriceup)
customer_email_entry.grid(row = 1, column=5,padx=50)

add_button = ttk.Button(items_frame, text="remove Item from DB"
                        ,command=removeitemtoDB)
add_button.grid(row=1,column=6,padx=1,pady=1,ipadx=10,ipady=10)




item_frame = Frame(root,bd=8, bg="#696969", relief=GROOVE)
item_frame.place(x=650,y=140,height=220,width=730)

item_title_label = Label(item_frame, text="Item", 
                    font=("times new roman", 20, "bold"),bg = "#696969", fg="white")
item_title_label.pack(side=TOP,fill="x")

item_frame2 = Frame(item_frame, bg="#696969")
item_frame2.pack(fill=X)

item_name_label = Label(item_frame2, text="Name", 
                    font=("times new roman", 12, "bold"),bg = "#696969", fg="white")
item_name_label.grid(row=0,column=0)

itemCategory = StringVar()
itemCategory.set("")

itemName = StringVar()
itemName.set("")
item_name = Entry(item_frame2, font="arial 12",textvariable=itemName,state=DISABLED, width=25)
item_name.grid(row=0,column=1,padx=10)

item_rate_label = Label(item_frame2, text="Rate", 
                    font=("arial", 12, "bold"),bg = "#696969", fg="white")
item_rate_label.grid(row=0,column=2,padx=40)

itemRate = StringVar()
itemRate.set("")
item_rate = Entry(item_frame2, font="arial 12",textvariable=itemRate,state=DISABLED, width=10)
item_rate.grid(row=0,column=3,padx=10)

item_quantity_label = Label(item_frame2, text="Quantity", 
                    font=("arial", 12, "bold"),bg = "#696969", fg="white")
item_quantity_label.grid(row=1,column=0,padx=30,pady=15)

itemQuantity = StringVar()
itemQuantity.set("")
item_quantity = Entry(item_frame2, font="arial 12",textvariable=itemQuantity, width=10)
item_quantity.grid(row=1,column=1)

item_frame3 = Frame(item_frame, bg="#696969")
item_frame3.pack(fill=X)



add_button = ttk.Button(item_frame3, text="Add Item",width=10
                        ,command=add_button_operation)
add_button.grid(row=0,column=0,padx=40,pady=10,ipadx=10,ipady=10)

remove_button = ttk.Button(item_frame3, text="Remove Item"
                        ,command=remove_button_operation)
remove_button.grid(row=0,column=1,padx=40,pady=30,ipadx=10,ipady=10)

update_button = ttk.Button(item_frame3, text="Update Quantity"
                        ,command=update_button_operation)
update_button.grid(row=0,column=2,padx=40,pady=30,ipadx=10,ipady=10)

clear_button = ttk.Button(item_frame3, text="Clear",
                        width=8,command=clear_button_operation,)
clear_button.grid(row=0,column=3,padx=40,pady=30,ipadx=10,ipady=10,sticky = W)


order_frame = Frame(root,bd=8, bg="#696969", relief=GROOVE)
order_frame.place(x=650,y=345,height=280,width=730)

order_title_label = Label(order_frame, text="Your Order", 
                    font=("times new roman", 20, "bold"),bg = "#696969", fg="white")
order_title_label.pack(side=TOP,fill="x")


order_tabel_frame = Frame(order_frame)
order_tabel_frame.place(x=0,y=40,height=180,width=720)

scrollbar_order_x = Scrollbar(order_tabel_frame,orient=HORIZONTAL)
scrollbar_order_y = Scrollbar(order_tabel_frame,orient=VERTICAL)

order_tabel = ttk.Treeview(order_tabel_frame,
            columns =("name","rate","quantity","price","category"),xscrollcommand=scrollbar_order_x.set,
            yscrollcommand=scrollbar_order_y.set)

order_tabel.heading("name",text="Name")
order_tabel.heading("rate",text="Rate")
order_tabel.heading("quantity",text="Quantity")
order_tabel.heading("price",text="Price")
order_tabel["displaycolumns"]=("name", "rate","quantity","price")
order_tabel["show"] = "headings"
order_tabel.column("rate",width=100,anchor='center', stretch=NO)
order_tabel.column("quantity",width=100,anchor='center', stretch=NO)
order_tabel.column("price",width=100,anchor='center', stretch=NO)

order_tabel.bind("<ButtonRelease-1>",load_item_from_order)

scrollbar_order_x.pack(side=BOTTOM,fill=X)
scrollbar_order_y.pack(side=RIGHT,fill=Y)

scrollbar_order_x.configure(command=order_tabel.xview)
scrollbar_order_y.configure(command=order_tabel.yview)

order_tabel.pack(fill=BOTH,expand=1)


total_price_label = Label(order_frame, text="Total",font=("arial", 12, "bold"),bg = "#696969", fg="white")
total_price_label.pack(side=LEFT,anchor=SW,padx=20,pady=10)

totalPrice = StringVar()
totalPrice.set("")
total_price_entry = Entry(order_frame, font="arial 12",textvariable=totalPrice,state=DISABLED,width=8)
total_price_entry.pack(side=LEFT,anchor=SW,padx=10,pady=10)

bill_button = ttk.Button(order_frame, text="Bill",width=15,
                        command=bill_button_operation)
bill_button.pack(side=LEFT,anchor=SW,padx=20,pady=10,ipadx=10,ipady=4)

unbill_button = ttk.Button(order_frame, text="UNP-Bill",width=15,command=Unpaid)
unbill_button.pack(side=LEFT,anchor=SW,padx=20,pady=10,ipadx=10,ipady=4)

cancel_button = ttk.Button(order_frame, text="Reset",width=15,command=cancel_button_operation)
cancel_button.pack(side=LEFT,anchor=SW,padx=20,pady=10,ipadx=10,ipady=4)



root.mainloop()