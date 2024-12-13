import tkinter as tk
import os
from tkinter import ttk
from tkinter import *
import webbrowser
from tkinter import messagebox
import pymysql
window = tk.Tk()

# def Exitpage():
#     sure = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=window)
#     if sure == True:
#         window.quit()
#
# window.protocol("WM_DELETE_WINDOW", Exitpage)
def shutdown():
    return os.system("shutdown /s /t 1")

def search():
    url = enter.get()
    webbrowser.open(url)

def search_box(event):
    if enter.get() == '  Search...':
        enter.delete(0, END)

def hide_indicate():
    b1_indicate.config(bg="#434343")
    b2_indicate.config(bg="#434343")
    b3_indicate.config(bg="#434343")
    b4_indicate.config(bg="#434343")
    b6_indicate.config(bg="#434343")

def indicate(lb, page):
    hide_indicate()
    lb.config(bg="#0066FF")
    delete_page()
    page()

# home elemenet
def home_page():
    home_frame = tk.Frame(main_frame)

    # Fetch data from the database
    total_orders = fetch_total_orders()
    total_employees = fetch_total_employees()
    total_food = fetch_total_food()

    # Labels displaying the fetched data
    one = tk.Label(home_frame, text='', bg="red")
    one.place(x=100, y=155, width=140, height=5)
    ans = tk.Label(home_frame,text="Total Order",font=('Californian FB', 18))
    ans.place(x=100, y=120, width=140)

    one_item = tk.Label(home_frame, text=total_orders, font=('Californian FB', 30))
    one_item.place(x=100, y=180, width=140)

    two = tk.Label(home_frame, text='', bg="red")
    two.place(x=500, y=155, width=150, height=5)
    two_item = tk.Label(home_frame, text="Total Employee", font=('Californian FB', 18))
    two_item.place(x=495, y=120, width=160)
    ans = tk.Label(home_frame, text=total_employees, font=('Californian FB', 30))
    ans.place(x=495, y=180, width=160)
    three = tk.Label(home_frame, text='', bg="red")
    three.place(x=900, y=155, width=150, height=5)
    three_item = tk.Label(home_frame, text="Total Food", font=('Californian FB', 18))
    three_item.place(x=900, y=120, width=160)
    ans = tk.Label(home_frame, text=total_food, font=('Californian FB', 30))
    ans.place(x=900, y=180, width=160)

    img = PhotoImage(file="diagram.png")  # Replace "path_to_your_image.png" with the actual path to your image

    # Create a label to display the image
    image_label = Label(home_frame, image=img)
    image_label.image = img  # Keep a reference to the image
    image_label.place(x=150, y=300)

    img = PhotoImage(file="pie-chart.png")
    image_label = Label(home_frame, image=img)
    image_label.image = img
    image_label.place(x=650, y=300)

    home_frame.pack(fill=tk.BOTH, expand=True)

# Functions to fetch data from the database
def fetch_total_orders():
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM placefood")  # Assuming 'orders' is your table name
    total_orders = cursor.fetchone()[0]
    conn.close()
    return total_orders

def fetch_total_employees():
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM addemployee")  # Assuming 'employees' is your table name
    total_employees = cursor.fetchone()[0]
    conn.close()
    return total_employees

def fetch_total_food():
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM addfood")  # Assuming 'food_items' is your table name
    total_food = cursor.fetchone()[0]
    conn.close()
    return total_food

def connection():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='Admin@21',
        db='pythonpro'
    )
    return conn


def fetch_food_items():
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT fname FROM addfood")
    food_items = cursor.fetchall()
    conn.close()
    return [item[0] for item in food_items]


def fetch_food_price(food_name):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT price FROM addfood WHERE fname=%s", (food_name,))
    price = cursor.fetchone()
    conn.close()
    return price[0] if price else 0


def fetch_delivery_boys():
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT fname FROM addemployee WHERE post='Delivery Boy'")
    delivery_boys = cursor.fetchall()
    conn.close()
    return [boy[0] for boy in delivery_boys]
def fetch_orders():
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, fname, quanti, total, address, payment, delivery FROM placefood")
    orders = cursor.fetchall()
    conn.close()
    return orders

def populate_treeview():
    global my_tree
    for row in my_tree.get_children():
        my_tree.delete(row)
    orders = fetch_orders()
    for order in orders:
        my_tree.insert('', 'end', values=order)

def on_food_selected(event):
    global unit_price
    selected_food = food_combobox.get()
    unit_price = fetch_food_price(selected_food)
    update_total_price()

def update_total_price(*args):
    quantity = int(quantity_spinbox.get())
    total_price = unit_price * quantity
    price_entry.delete(0, tk.END)
    price_entry.insert(0, str(total_price))

def insert_order():
    name = name_entry.get()
    food = food_combobox.get()
    quantity = int(quantity_spinbox.get())
    total_amt = price_entry.get()
    address = address_entry.get()
    payment_method = radio.get()
    delivery_boy = delivery_combobox.get()
    payment_methods = {1: 'Cash', 2: 'Online', 3: 'Cards'}
    payment = payment_methods.get(payment_method, 'Unknown')

    # Validate inputs
    if not name or not food or not quantity or not total_amt or not address or payment_method == 0 or not delivery_boy:
        messagebox.showerror("Input Error", "All fields are required.")
        return

    conn = connection()
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO placefood (name, fname, quanti, total, address, payment, delivery)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (name, food, quantity, total_amt, address, payment, delivery_boy))
    conn.commit()
    conn.close()

    # Clear the fields after submission
    name_entry.delete(0, tk.END)
    food_combobox.set('')
    quantity_spinbox.delete(0, tk.END)
    quantity_spinbox.insert(0, 0)
    price_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
    radio.set(0)
    delivery_combobox.set('')

    # Populate the treeview with updated data
    populate_treeview()

def Categories_page():
    global my_tree
    global food_combobox, price_entry, quantity_spinbox, unit_price, name_entry, address_entry, radio, delivery_combobox

    unit_price = 0

    order = tk.Frame(main_frame)
    order.pack(fill=tk.BOTH, expand=True)

    title = Label(order, text='Starbucks', font=('Monotype Corsiva', 36))
    title.place(x=10, y=30)

    # Name field
    name = Label(order, text="Name: ", fg="#4f4e4d", font=("yu gothic ui", 13, "bold"))
    name.place(x=150, y=157)
    name_entry = Entry(order, highlightthickness=0, relief=FLAT, bg="white", fg="#6b6a69",
                       font=("yu gothic ui semibold", 12))
    name_entry.place(x=250, y=160, width=209)
    name_line = Canvas(order, width=209, height=2.5, bg="#bdb9b1", highlightthickness=0)
    name_line.place(x=250, y=184)

    # Food combobox
    food = Label(order, text="Food:", fg="#4f4e4d", font=("yu gothic ui", 13, "bold"))
    food.place(x=150, y=200)
    food_combobox = ttk.Combobox(order, foreground="#6b6a69", font=("yu gothic ui semibold", 12))
    food_combobox['values'] = fetch_food_items()
    food_combobox.place(x=250, y=200, width=209)
    food_combobox.bind("<<ComboboxSelected>>", on_food_selected)
    food_line = Canvas(order, width=200, height=1.5, bg="#bdb9b1", highlightthickness=0)
    food_line.place(x=250, y=225)

    # Quantity spinbox
    con = Label(order, text="Quantity: ", fg="#4f4e4d", font=("yu gothic ui", 13, "bold"))
    con.place(x=150, y=250)
    quantity_spinbox = Spinbox(order, from_=0, to=100, width=22, font=("yu gothic ui", 12), command=update_total_price)
    quantity_spinbox.place(x=250, y=250)
    quantity_spinbox.bind("<KeyRelease>", update_total_price)  # Ensure it updates on key input
    quantity_spinbox.bind("<ButtonRelease>", update_total_price)  # Ensure it updates on button release

    # Total amount field
    price = Label(order, text="Total AMT: ", fg="#4f4e4d", font=("yu gothic ui", 13, "bold"))
    price.place(x=150, y=300)
    price_entry = Entry(order, highlightthickness=0, relief=FLAT, bg="white", fg="#6b6a69",
                        font=("yu gothic ui semibold", 12))
    price_entry.place(x=250, y=300, width=209)
    price_line = Canvas(order, width=209, height=1.5, bg="#bdb9b1", highlightthickness=0)
    price_line.place(x=250, y=324)

    # Address field
    address = Label(order, text="Address: ", fg="#4f4e4d", font=("yu gothic ui", 13, "bold"))
    address.place(x=150, y=350)
    address_entry = Entry(order, highlightthickness=0, relief=FLAT, bg="white", fg="#6b6a69",
                          font=("yu gothic ui semibold", 12))
    address_entry.place(x=250, y=350, width=209)
    address_line = Canvas(order, width=209, height=2.5, bg="#bdb9b1", highlightthickness=0)
    address_line.place(x=250, y=374)

    # Payment method radio buttons
    radio = IntVar()
    lb = Label(order, text="Payments:", fg="#4f4e4d", font=("yu gothic ui", 13, "bold"))
    lb.place(x=150, y=400)
    b1 = Radiobutton(order, text='Cash', font=("yu gothic ui", 13, "bold"), fg="#4f4e4d", variable=radio, value=1,
                     anchor=W)
    b1.place(x=250, y=400)
    b2 = Radiobutton(order, text='Online', font=("yu gothic ui", 13, "bold"), fg="#4f4e4d", variable=radio, value=2,
                     anchor=W)
    b2.place(x=250, y=430)
    b3 = Radiobutton(order, text='Cards', font=("yu gothic ui", 13, "bold"), fg="#4f4e4d", variable=radio, value=3,
                     anchor=W)
    b3.place(x=250, y=460)

    # Delivery Boy combobox
    temp = Label(order, text='Delivery Boy:', fg="#4f4e4d", font=("yu gothic ui", 13, "bold"))
    temp.place(x=150, y=500)
    delivery_combobox = ttk.Combobox(order, foreground="#6b6a69", font=("yu gothic ui semibold", 12))
    delivery_combobox['values'] = fetch_delivery_boys()
    delivery_combobox.place(x=260, y=500)
    delivery_line = Canvas(order, width=200, height=1.5, bg="#bdb9b1", highlightthickness=0)
    delivery_line.place(x=260, y=525)

    # Submit button
    submit_button = Button(order, text="Submit", height=0, width=10, bd=0, bg='#E88B8B',
                           activebackground="#fff", cursor='hand2', fg="#4f4e4d", font=("yu gothic ui", 20, "bold"),
                           command=insert_order)
    submit_button.place(x=240, y=570)

    # Treeview for displaying order details
    my_tree = ttk.Treeview(order)
    my_tree['columns'] = ("name", "fname", "qon", "total", "Add", "pay", "dil")
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("name", anchor=W, width=100)
    my_tree.column("fname", anchor=W, width=100)
    my_tree.column("qon", anchor=W, width=100)
    my_tree.column("total", anchor=W, width=100)
    my_tree.column("Add", anchor=W, width=100)
    my_tree.column("pay", anchor=W, width=100)
    my_tree.column("dil", anchor=W, width=125)

    my_tree.heading("name", text="Name", anchor=W)
    my_tree.heading("fname", text="Food Name", anchor=W)
    my_tree.heading("qon", text="Quantity", anchor=W)
    my_tree.heading("total", text="Total AMT", anchor=W)
    my_tree.heading("Add", text="Address", anchor=W)
    my_tree.heading("pay", text="Payment", anchor=W)
    my_tree.heading("dil", text="Delivery Boy", anchor=W)
    my_tree.place(x=510, y=150, height=400)
    populate_treeview()
    order.pack(fill=tk.BOTH, expand=True)
def menu_page():
    menu_frame = tk.Frame(main_frame)
    title = Label(menu_frame, text='Starbucks', font=('Monotype Corsiva', 36))
    title.place(x=10, y=30)

    subtitle = Label(menu_frame, text='Menu list', font=('Monotype Corsiva', 18))
    subtitle.place(x=130, y=80)

    tree = ttk.Treeview(menu_frame)
    tree['columns'] = ("Id", "Name", "Price", "Category")  # Adjusted "name" to "Name" for consistency
    tree.column("#0", width=0, stretch=NO)
    tree.column("Id", anchor=W, width=70)
    tree.column("Name", anchor=W, width=150)  # Adjusted "name" to "Name" for consistency
    tree.column("Price", anchor=W, width=150)
    tree.column("Category", anchor=W, width=150)

    tree.heading("Id", text="ID", anchor=W)
    tree.heading("Name", text="Food Name", anchor=W)  # Adjusted "name" to "Name" for consistency
    tree.heading("Price", text="Price", anchor=W)
    tree.heading("Category", text="Category", anchor=W)

    # Populate the Treeview with data from the database
    populate_menu_tree(tree)

    tree.place(x=250, y=150, height=400, width=700)

    menu_frame.pack(fill=tk.BOTH, expand=True)

def populate_menu_tree(tree):
    # Fetch data from the database
    menu_data = fetch_menu_data()

    # Insert data into the Treeview
    for item in menu_data:
        tree.insert('', 'end', values=item)

def fetch_menu_data():
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM addfood")  # Adjust SQL query according to your table structure
    menu_data = cursor.fetchall()
    conn.close()
    return menu_data

def Staff_page():
    Staff_frame = tk.Frame(main_frame)
    title = Label(Staff_frame, text='Starbucks', font=('Monotype Corsiva', 36))
    title.place(x=10, y=30)

    subtitle = Label(Staff_frame, text='Orders', font=('Monotype Corsiva', 18))
    subtitle.place(x=130, y=80)

    my_tree = ttk.Treeview(Staff_frame)
    my_tree['columns'] = ("Name", "Food Name", "Quantity", "Total AMT", "Address", "Payment", "Delivery Boy")
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("Name", anchor=W, width=100)
    my_tree.column("Food Name", anchor=W, width=100)
    my_tree.column("Quantity", anchor=W, width=100)
    my_tree.column("Total AMT", anchor=W, width=100)
    my_tree.column("Address", anchor=W, width=150)
    my_tree.column("Payment", anchor=W, width=100)
    my_tree.column("Delivery Boy", anchor=W, width=125)

    my_tree.heading("Name", text="Name", anchor=W)
    my_tree.heading("Food Name", text="Food Name", anchor=W)
    my_tree.heading("Quantity", text="Quantity", anchor=W)
    my_tree.heading("Total AMT", text="Total AMT", anchor=W)
    my_tree.heading("Address", text="Address", anchor=W)
    my_tree.heading("Payment", text="Payment", anchor=W)
    my_tree.heading("Delivery Boy", text="Delivery Boy", anchor=W)

    # Populate the Treeview with data from the database
    populate_staff_orders_tree(my_tree)

    my_tree.place(x=300, y=150, height=400)

    Staff_frame.pack(fill=tk.BOTH, expand=True)

def populate_staff_orders_tree(tree):
    # Fetch data from the database
    staff_orders_data = fetch_staff_orders_data()

    # Insert data into the Treeview
    for item in staff_orders_data:
        tree.insert('', 'end', values=item)

def fetch_staff_orders_data():
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, fname, quanti, total, address, payment, delivery FROM placefood")  # Assuming 'placefood' is your table name
    staff_orders_data = cursor.fetchall()
    conn.close()
    return staff_orders_data


def Reports_page():
    Reports_frame = tk.Frame(main_frame)
    lb = tk.Label(Reports_frame, text='Reports_frame page \n\n page 1', font=('Californian FB', 32))
    lb.pack()

    Reports_frame.pack(pady=20)

def delete_page():
    for frame in main_frame.winfo_children():
        frame.destroy()

window.geometry("1520x790+0+0")
window.title("Food Delivery Management")
window.resizable(1, 1)
window.configure(bg="#fff")
def loginopen():
    import login
def Logout_page():
    Logout_frame = tk.Frame(main_frame)
    sure = messagebox.askyesno("Exit", "Are you sure to LogOut?", parent=window)
    if sure == True:
        window.destroy()
        loginopen()

# # Set the protocol for closing the window
window.protocol("logout", Logout_page)

# home_page()
frame = Frame(window, width=260, height=777, bg="#434343")
frame.place(x=0, y=5)

frame2 = Frame(window, width=1250, height=60, bg="#0066FF")
frame2.place(x=261, y=5)
# enter = Entry(window,width=35,bg="red")
enter = (Entry(window, width=30, font=('Californian FB', 15,), fg="#000"
               , cursor='hand2'))

enter.place(x=350, y=20)
enter.insert(0, '  Search...')
enter.bind('<FocusIn>', search_box)

searching = PhotoImage(file='search2.png')
sci = Button(window, image=searching, command=search, bd=0, bg="#0066FF", activebackground="#0066FF", cursor='hand2')
sci.place(x=690, y=20)

main_frame = tk.Frame(window, highlightbackground='black', highlightthickness=1)
main_frame.place(x=261, y=68)
main_frame.pack_propagate(False)
main_frame.configure(height=712, width=1250)
home_page()

icon = PhotoImage(file='Starbucks-removebg.png')
logo = tk.Label(window, image=icon, bd=0, cursor='hand2')
logo.place(x=0, y=15)

picolumen = PhotoImage(file='list.png')
menu = tk.Label(window, image=picolumen, cursor='hand2', bg="#0066FF")
menu.place(x=270, y=20)

Shut = PhotoImage(file='shutswonimg.png')
shutlogo = tk.Button(window, image=Shut, bd=0, bg="#434343", cursor='hand2', activebackground="#434343",
                     command=shutdown)
shutlogo.place(x=1, y=650)

shut = Button(window, text="ShutDown", font=('Bell MT', 23, 'bold'), bd=0, activebackground="#434343", bg="#434343"
              , cursor='hand2', fg="#b1a4a5", command=shutdown)
shut.place(x=50, y=650)

b1 = Button(window, text="Home", font=('Californian FB', 20), bd=0, activebackground="#434343", bg="#434343"
            , cursor='hand2', fg="#b1a4a5", command=lambda: indicate(b1_indicate, home_page))
b1.place(x=50, y=150)
b1_indicate = tk.Label(window, text='', bg="#434343")
b1_indicate.place(x=50, y=195, width=100, height=5)
home = PhotoImage(file='3d-house.png')
homeicon = tk.Button(window, image=home, bd=0, bg="#434343", cursor='hand2', activebackground="#434343")
homeicon.place(x=5, y=150)

b2 = Button(window, text="Place Order", font=('Californian FB', 20), bd=0, activebackground="#434343", bg="#434343"
            , cursor='hand2', fg="#b1a4a5", command=lambda: indicate(b2_indicate, Categories_page))
b2.place(x=50, y=210)
b2_indicate = tk.Label(window, text='', bg="#434343")
b2_indicate.place(x=50, y=255, width=150, height=5)
Categorie = PhotoImage(file='application.png')
Categorieicon = tk.Button(window, image=Categorie, bd=0, bg="#434343", cursor='hand2', activebackground="#434343")
Categorieicon.place(x=5, y=210)

b3 = Button(window, text="Menu", font=('Californian FB', 20), bd=0, activebackground="#434343", bg="#434343"
            , cursor='hand2', fg="#b1a4a5", command=lambda: indicate(b3_indicate, menu_page))
b3.place(x=50, y=270)
b3_indicate = tk.Label(window, text='', bg="#434343")
b3_indicate.place(x=50, y=315, width=100, height=5)
Menu = PhotoImage(file='list2.png')
Menuicon = tk.Button(window, image=Menu, bd=0, bg="#434343", cursor='hand2', activebackground="#434343")
Menuicon.place(x=5, y=270)

b4 = Button(window, text="Order", font=('Californian FB', 20), bd=0, activebackground="#434343", bg="#434343"
            , cursor='hand2', fg="#b1a4a5", command=lambda: indicate(b4_indicate, Staff_page))
b4.place(x=50, y=330)
b4_indicate = tk.Label(window, text='', bg="#434343")
b4_indicate.place(x=50, y=375, width=100, height=5)
Staff = PhotoImage(file='man.png')
Stafficon = tk.Button(window, image=Staff, bd=0, bg="#434343", cursor='hand2', activebackground="#434343")
Stafficon.place(x=5, y=330)


b6 = Button(window, text="Logout", font=('Californian FB', 20), bd=0, activebackground="#434343", bg="#434343"
            , cursor='hand2', fg="#b1a4a5", command=lambda: indicate(b6_indicate, Logout_page))
b6.place(x=50, y=390)
b6_indicate = tk.Label(window, text='', bg="#434343")
b6_indicate.place(x=50, y=495, width=100, height=5)
Logout = PhotoImage(file='check-out.png')
Logouticon = tk.Button(window, image=Logout, bd=0, bg="#434343", cursor='hand2', activebackground="#434343")
Logouticon.place(x=5, y=390)

window.mainloop()