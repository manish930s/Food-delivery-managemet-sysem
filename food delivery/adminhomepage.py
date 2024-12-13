import os
import tkinter as tk
import webbrowser
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymysql
from datetime import datetime

window = tk.Tk()


# def Exit():
#     sure = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=window)
#     if sure == True:
#         window.quit()
#
#
# window.protocol("WM_DELETE_WINDOW", Exit)

def shutdown():
    return os.system("shutdown /s /t 1")


def search():
    url = enter.get()
    webbrowser.open(url)


def search_enter(event):
    if enter.get() == 'Search...':
        enter.delete(0, END)


def hide_indicate():
    b0_indicate.config(bg="#434343")
    b1_indicate.config(bg="#434343")
    b2_indicate.config(bg="#434343")
    b3_indicate.config(bg="#434343")
    b4_indicate.config(bg="#434343")
    b6_indicate.config(bg="#434343")


def delete_page():
    for frame in main_frame.winfo_children():
        frame.destroy()


def indicate(lb, page):
    hide_indicate()
    lb.config(bg="#0066FF")
    delete_page()
    page()


# home elemenet
def home_page():
    home_frame = tk.Frame(main_frame)

    total_orders = fetch_total_orders()
    total_employees = fetch_total_employees()
    total_food = fetch_total_food()
    total_income = calculate_total_income()

    # Labels displaying the fetched data
    one = tk.Label(home_frame, text='', bg="red")
    one.place(x=100, y=155, width=140, height=5)
    ans = tk.Label(home_frame, text="Total Order", font=('Californian FB', 18))
    ans.place(x=100, y=120, width=140)
    one_item = tk.Label(home_frame, text=total_orders, font=('Californian FB', 30))
    one_item.place(x=100, y=180, width=140)

    two = tk.Label(home_frame, text='', bg="red")
    two.place(x=400, y=155, width=150, height=5)
    two_item = tk.Label(home_frame, text="Total Employee", font=('Californian FB', 18))
    two_item.place(x=395, y=120, width=160)
    ans = tk.Label(home_frame, text=total_employees, font=('Californian FB', 30))
    ans.place(x=395, y=180, width=160)

    three = tk.Label(home_frame, text='', bg="red")
    three.place(x=700, y=155, width=150, height=5)
    three_item = tk.Label(home_frame, text="Total Food", font=('Californian FB', 18))
    three_item.place(x=700, y=120, width=160)
    ans = tk.Label(home_frame, text=total_food, font=('Californian FB', 30))
    ans.place(x=700, y=180, width=160)

    forr = tk.Label(home_frame, text='', bg="red")
    forr.place(x=1000, y=155, width=150, height=5)
    forr_item = tk.Label(home_frame, text="Total Income", font=('Californian FB', 18))
    forr_item.place(x=1000, y=120, width=160)
    ans = tk.Label(home_frame, text=total_income, font=('Californian FB', 30))
    ans.place(x=1000, y=180, width=160)

    # img = PhotoImage(file="diagram.png")  # Replace "path_to_your_image.png" with the actual path to your image

    # # Create a label to display the image
    # image_label = Label(home_frame, image=img)
    # image_label.image = img  # Keep a reference to the image
    # image_label.place(x=150, y=300)

    # img = PhotoImage(file="pie-chart.png")
    # image_label = Label(home_frame, image=img)
    # image_label.image = img
    # image_label.place(x=650, y=310)

    home_frame.pack(fill=tk.BOTH, expand=True)

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

def calculate_total_income():
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(total) FROM placefood")  # Assuming 'total_amt' is the column storing the total amount per order
    total_income = cursor.fetchone()[0]  # Fetching the total income
    conn.close()
    return total_income
def employee():
    home_frame = Frame(main_frame)

    def clear():
        position_comobox.delete(0, END)
        firstname_entery.delete(0, END)
        Surnamename_entery.delete(0, END)
        email_entery.delete(0, END)
        phoneno_entery.delete(0, END)
        password_entery.delete(0, END)
        conpass_entery.delete(0, END)
        DOB_entry.delete(0, END)
        join_entry.delete(0, END)
        DOB_entry.insert(0, "yyyy-mm-dd")
        join_entry.insert(0, "yyyy-mm-dd")

    def user_enter(event):
        if DOB_entry.get() == 'yyyy-mm-dd':
            DOB_entry.delete(0, END)

    def joinnn_enter(event):
        if join_entry.get() == 'yyyy-mm-dd':
            join_entry.delete(0, END)

    def connect_database():
        dob_str = DOB_entry.get()
        if position_comobox.get() == '' or firstname_entery.get() == '' or Surnamename_entery.get() == '' or email_entery.get() == '' or phoneno_entery.get() == '' or password_entery.get() == '' or conpass_entery.get() == '' or DOB_entry.get() == '' or join_entry.get() == '':
            messagebox.showerror('Error', 'All fields are Required')
        elif password_entery.get() != conpass_entery.get():
            messagebox.showerror('Error', 'Password Mismatch')
        else:
            try:
                con = pymysql.connect(host='localhost', user='root', password='Admin@21')
                mycursor = con.cursor()
            except:
                messagebox.showerror('Error', 'Database Connectivity Issue, Please Try Again')
                return
        try:
            query = 'create database pythonpro'
            mycursor.execute(query)
            query = 'use pythonpro'
            mycursor.execute(query)
            query = 'create table addemployee(id int auto_increment primary key not null, post varchar(40), fname varchar(50), sname varchar(50),email varchar(40), mobaile int,passwordd varchar(50), dob DATE ,joindate DATE )'
            mycursor.execute(query)
        except:
            mycursor.execute('use pythonpro')

        query = 'select * from addemployee where email= %s'
        mycursor.execute(query, (email_entery.get()))

        row = mycursor.fetchone()
        if row != None:
            messagebox.showerror('Error', 'Email ID Already exists')
        else:
            query = 'INSERT INTO addemployee(post, fname, sname, email, mobaile, passwordd, dob, joindate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
            mycursor.execute(query, (
            position_comobox.get(), firstname_entery.get(), Surnamename_entery.get(), email_entery.get(),
            phoneno_entery.get(), password_entery.get(), DOB_entry.get(), join_entry.get()))
            con.commit()
            con.close()
            messagebox.showinfo('Success', 'Registration is Successful')
            clear()

    title = Label(home_frame, text='Starbucks', font=('Monotype Corsiva', 36))
    title.place(x=10, y=30)

    subtitel = Label(home_frame, text='add employee', font=('Monotype Corsiva', 18))
    subtitel.place(x=130, y=80)

    position = Label(home_frame, text="position:", fg="#4f4e4d",
                     font=("yu gothic ui", 13, "bold"))
    position.place(x=600, y=157)
    position_comobox = ttk.Combobox(home_frame, foreground="#6b6a69", background="white",
                                    font=("yu gothic ui semibold", 12),
                                    values=["", "Manager","Delivery Boy"])
    position_comobox.place(x=800, y=160)
    position_line = Canvas(home_frame, width=200, height=1.5, bg="#bdb9b1", highlightthickness=0)
    position_line.place(x=800, y=184)

    firstname = Label(home_frame, text="First Name: ", fg="#4f4e4d",
                      font=("yu gothic ui", 13, "bold"))
    firstname.place(x=100, y=200)
    firstname_entery = (Entry(home_frame, highlightthickness=0, relief=FLAT, bg="white", fg="#6b6a69",
                              font=("yu gothic ui semibold", 12)))
    firstname_entery.place(x=200, y=200, width=260)
    f_name_line = Canvas(home_frame, width=260, height=1.5, bg="#bdb9b1", highlightthickness=0)
    f_name_line.place(x=200, y=224)

    Surnamename = Label(home_frame, text="Surname: ", fg="#4f4e4d",
                        font=("yu gothic ui", 13, "bold"))
    Surnamename.place(x=600, y=200)
    Surnamename_entery = (Entry(home_frame, highlightthickness=0, relief=FLAT, bg="white", fg="#6b6a69",
                                font=("yu gothic ui semibold", 12)))
    Surnamename_entery.place(x=750, y=200, width=260)
    s_name_line = Canvas(home_frame, width=260, height=1.5, bg="#bdb9b1", highlightthickness=0)
    s_name_line.place(x=750, y=224)

    email = Label(home_frame, text="Email ID: ", fg="#4f4e4d",
                  font=("yu gothic ui", 13, "bold"))
    email.place(x=100, y=250)
    email_entery = (Entry(home_frame, highlightthickness=0, relief=FLAT, bg="white", fg="#6b6a69",
                          font=("yu gothic ui semibold", 12)))
    email_entery.place(x=200, y=250, width=260)
    email_line = Canvas(home_frame, width=260, height=1.5, bg="#bdb9b1", highlightthickness=0)
    email_line.place(x=200, y=274)

    phoneno = Label(home_frame, text="Mobile no: ", fg="#4f4e4d",
                    font=("yu gothic ui", 13, "bold"))
    phoneno.place(x=600, y=250)
    phoneno_entery = (Entry(home_frame, highlightthickness=0, relief=FLAT, bg="white", fg="#6b6a69",
                            font=("yu gothic ui semibold", 12)))
    phoneno_entery.place(x=750, y=250, width=260)
    phoneno_line = Canvas(home_frame, width=260, height=1.5, bg="#bdb9b1", highlightthickness=0)
    phoneno_line.place(x=750, y=274)

    password = Label(home_frame, text="Password: ", fg="#4f4e4d",
                     font=("yu gothic ui", 13, "bold"))
    password.place(x=100, y=300)
    password_entery = (Entry(home_frame, highlightthickness=0, relief=FLAT, bg="white", fg="#6b6a69",
                             font=("yu gothic ui semibold", 12)))
    password_entery.place(x=200, y=300, width=260)
    password_line = Canvas(home_frame, width=260, height=1.5, bg="#bdb9b1", highlightthickness=0)
    password_line.place(x=200, y=324)

    conpass = Label(home_frame, text="Confirm Password: ", fg="#4f4e4d",
                    font=("yu gothic ui", 13, "bold"))
    conpass.place(x=590, y=300)
    conpass_entery = (Entry(home_frame, highlightthickness=0, relief=FLAT, bg="white", fg="#6b6a69",
                            font=("yu gothic ui semibold", 12)))
    conpass_entery.place(x=750, y=300, width=260)
    conpass_line = Canvas(home_frame, width=260, height=1.5, bg="#bdb9b1", highlightthickness=0)
    conpass_line.place(x=750, y=324)

    DOB_label = Label(home_frame, text="DOB: ", fg="#4f4e4d",
                      font=("yu gothic ui", 13, "bold"))
    DOB_label.place(x=100, y=360)
    DOB_entry = (Entry(home_frame, highlightthickness=0, relief=FLAT, bg="white", fg="#6b6a69",
                       font=("yu gothic ui semibold", 12)))
    DOB_entry.insert(0, "yyyy-mm-dd")
    DOB_entry.place(x=200, y=360, width=255)  # trebuchet ms
    DOB_entry.bind('<FocusIn>', user_enter)
    DOB_entryline = Canvas(home_frame, width=255, height=1.5, bg="#bdb9b1", highlightthickness=0)
    DOB_entryline.place(x=200, y=384)

    Join_label = Label(home_frame, text="Joing Date: ", fg="#4f4e4d",
                       font=("yu gothic ui", 13, "bold"))
    Join_label.place(x=600, y=360)
    join_entry = (Entry(home_frame, highlightthickness=0, relief=FLAT, bg="white", fg="#6b6a69",
                        font=("yu gothic ui semibold", 12)))
    join_entry.insert(0, "yyyy-mm-dd")
    join_entry.place(x=750, y=360, width=255)  # trebuchet ms
    join_entry.bind('<FocusIn>', joinnn_enter)
    join_entryline = Canvas(home_frame, width=255, height=1.5, bg="#bdb9b1", highlightthickness=0)
    join_entryline.place(x=750, y=385)

    submitButton = Button(home_frame, text="Submit", height=1, width=25, bd=0, bg='#E88B8B',
                          activebackground="#fff", cursor='hand2', fg="#4f4e4d", font=("yu gothic ui", 25, "bold"),
                          command=connect_database)
    submitButton.place(x=300, y=500)

    home_frame.pack(fill=tk.BOTH, expand=True)


def list():
    emplist = Frame(main_frame)

    conn = connection()
    cursor = conn.cursor()

    def read():
        cursor.connection.ping()
        sql = f"SELECT * FROM addemployee where `post` = 'Manager'"
        cursor.execute(sql)
        results = cursor.fetchall()
        conn.commit()
        conn.close()
        return results

    def refreshTable():
        for data in my_tree.get_children():
            my_tree.delete(data)
        for array in read():
            my_tree.insert(parent='', index='end', iid=array, text="", values=(array), tag="orow")
        my_tree.tag_configure('orow', background="#EEEEEE")
        my_tree.pack()

    title = Label(emplist, text='Starbucks', font=('Monotype Corsiva', 36))
    title.place(x=10, y=30)

    subtitel = Label(emplist, text='employee list', font=('Monotype Corsiva', 18))
    subtitel.place(x=130, y=80)

    my_tree = ttk.Treeview(emplist)
    my_tree['columns'] = ("Id", "post", "name", "Surname", "Email", "Mobail no.", "Password", "DOB", "Joining Date")
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("Id", anchor=W, width=70)
    my_tree.column("post", anchor=W, width=100)
    my_tree.column("name", anchor=W, width=125)
    my_tree.column("Surname", anchor=W, width=100)
    my_tree.column("Email", anchor=W, width=150)
    my_tree.column("Mobail no.", anchor=W, width=125)
    my_tree.column("Password", anchor=W, width=100)
    my_tree.column("DOB", anchor=W, width=100)
    my_tree.column("Joining Date", anchor=W, width=100)

    my_tree.heading("Id", text="ID", anchor=W)
    my_tree.heading("post", text="Post", anchor=W)
    my_tree.heading("name", text="Name", anchor=W)
    my_tree.heading("Surname", text="Surname", anchor=W)
    my_tree.heading("Email", text="Email", anchor=W)
    my_tree.heading("Mobail no.", text="Mobile no.", anchor=W)
    my_tree.heading("Password", text="Password", anchor=W)
    my_tree.heading("DOB", text="DOB", anchor=W)
    my_tree.heading("Joining Date", text="Joining Date", anchor=W)
    refreshTable()
    my_tree.place(x=150, y=230, height=400)

    emplist.pack(fill=tk.BOTH, expand=True)


def connection():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='Admin@21',
        db='pythonpro'
    )
    return conn


def Dellivery_boy():
    delivery = tk.Frame(main_frame)
    conn = connection()
    cursor = conn.cursor()

    def read():
        cursor.connection.ping()
        sql = f"SELECT * FROM addemployee where `post` = 'delivery boy' "
        cursor.execute(sql)
        results = cursor.fetchall()
        conn.commit()
        conn.close()
        return results

    def refreshTable():
        for data in my_tree.get_children():
            my_tree.delete(data)
        for array in read():
            my_tree.insert(parent='', index='end', text="", values=(array))
        my_tree.tag_configure('orow', background="#EEEEEE")
        my_tree.pack()

    title = Label(delivery, text='Starbucks', font=('Monotype Corsiva', 36))
    title.place(x=10, y=30)
    subtitel = Label(delivery, text='employee list', font=('Monotype Corsiva', 18))
    subtitel.place(x=130, y=80)

    my_tree = ttk.Treeview(delivery)
    my_tree['columns'] = ("Id", "post", "name", "Surname", "Email", "Mobail no.", "Password", "DOB", "Joining Date")
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("Id", anchor=W, width=70)
    my_tree.column("post", anchor=W, width=100)
    my_tree.column("name", anchor=W, width=125)
    my_tree.column("Surname", anchor=W, width=100)
    my_tree.column("Email", anchor=W, width=150)
    my_tree.column("Mobail no.", anchor=W, width=125)
    my_tree.column("Password", anchor=W, width=100)
    my_tree.column("DOB", anchor=W, width=100)
    my_tree.column("Joining Date", anchor=W, width=100)

    my_tree.heading("Id", text="ID", anchor=W)
    my_tree.heading("post", text="Post", anchor=W)
    my_tree.heading("name", text="Name", anchor=W)
    my_tree.heading("Surname", text="Surname", anchor=W)
    my_tree.heading("Email", text="Email", anchor=W)
    my_tree.heading("Mobail no.", text="Mobail no.", anchor=W)
    my_tree.heading("Password", text="Password", anchor=W)
    my_tree.heading("DOB", text="DOB", anchor=W)
    my_tree.heading("Joining Date", text="Joining Date", anchor=W)
    refreshTable()
    my_tree.place(x=150, y=230, height=400)

    delivery.pack(fill=tk.BOTH, expand=True)


def addfood():
    food = tk.Frame(main_frame)
    conn = connection()
    mycursor = conn.cursor()

    def temp(event):
        select_tree = tree.focus()
        if select_tree:
            row = tree.item(select_tree)['values']
            clear()
            foodname_entery.insert(0, row[1])
            price_entery.insert(0, row[2])
            Categorie_comobox.set(row[3])
        else:
            pass

    tree = ttk.Treeview(food)
    tree['columns'] = ("Id", "name", "Price", "Categories")
    tree.column("#0", width=0, stretch=NO)
    tree.column("Id", anchor=W, width=70)
    tree.column("name", anchor=W, width=125)
    tree.column("Price", anchor=W, width=125)
    tree.column("Categories", anchor=W, width=125)

    tree.heading("Id", text="ID", anchor=W)
    tree.heading("name", text="Food Name", anchor=W)
    tree.heading("Price", text="Price", anchor=W)
    tree.heading("Categories", text="Categories", anchor=W)
    tree.bind('<ButtonRelease>', temp)
    # refreshTable()
    tree.place(x=700, y=150, height=400)

    def clear():
        foodname_entery.delete(0,END)
        price_entery.delete(0,END)
        Categorie_comobox.delete(0, END)

    def read(tree):
        sql = f"SELECT * FROM addfood"
        mycursor.execute(sql)
        results = mycursor.fetchall()
        for data in tree.get_children():
            tree.delete(data)
        for array in results:
            tree.insert('',END, values=array)
        conn.commit()
        conn.close()
        return results

    def save():
        name = foodname_entery.get().strip()
        price = price_entery.get().strip()
        cat = Categorie_comobox.get().strip()

        if not name or not price or not cat:
            messagebox.showwarning("", "Please fill up all entries")
            return

        try:
            conn = connection()
            mycursor = conn.cursor()

            query = 'SELECT * FROM addfood WHERE fname = %s'
            mycursor.execute(query, (name,))
            row = mycursor.fetchone()

            if row:
                messagebox.showerror('Error', 'Food already exists')
            else:
                query = 'INSERT INTO addfood (fname, price, categorie) VALUES (%s, %s, %s)'
                mycursor.execute(query, (name, price, cat))
                conn.commit()
                messagebox.showinfo('Success', 'Registration is Successful')
                clear()
                read(tree)

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

        finally:
            mycursor.close()
            conn.close()

    def delete():
        select_item = tree.focus()
        if not select_item:
            messagebox.showerror('Error', 'Choose a food to delete.')
        else:
            try:
                conn = connection()
                mycursor = conn.cursor()
                food_name = foodname_entery.get().strip()
                query = 'DELETE FROM addfood WHERE fname = %s'
                mycursor.execute(query, (food_name,))
                conn.commit()
                messagebox.showinfo('Success', 'Data has been deleted.')
                clear()
                read(tree)
            except Exception as e:
                conn.rollback()
                messagebox.showerror('Error', f'An error occurred: {str(e)}')
            finally:
                mycursor.close()
                conn.close()

    def update():
        select_item = tree.focus()
        if not select_item:
            messagebox.showerror('Error', 'Choose a food to update.')
        else:
            conn = None
            mycursor = None
            try:
                item_values = tree.item(select_item)['values']
                if item_values and len(item_values) >= 1:
                    select_id = item_values[0]
                else:
                    raise ValueError("No valid ID found for the selected food.")

                conn = connection()
                mycursor = conn.cursor()

                query = 'UPDATE addfood SET fname = %s, price = %s, categorie = %s WHERE id = %s'
                mycursor.execute(query, (foodname_entery.get(), price_entery.get(), Categorie_comobox.get(), select_id))
                conn.commit()
                messagebox.showinfo('Success', 'Data has been updated.')
                clear()
                read(tree)
            except ValueError as ve:
                messagebox.showerror('Error', str(ve))
            except Exception as e:
                if conn:
                    conn.rollback()
                messagebox.showerror('Error', f'An error occurred: {str(e)}')
            finally:
                if mycursor:
                    mycursor.close()
                if conn:
                    conn.close()

    read(tree)
    title = Label(food, text='Starbucks', font=('Monotype Corsiva', 36))
    title.place(x=10, y=30)
    subtitel = Label(food, text='add Food', font=('Monotype Corsiva', 18))
    subtitel.place(x=130, y=80)
    foodname = Label(food, text="Food Name: ", fg="#4f4e4d",
                     font=("yu gothic ui", 13, "bold"))
    foodname.place(x=100, y=200)
    foodname_entery = (Entry(food, highlightthickness=0, relief=FLAT, bg="white", fg="#6b6a69",
                             font=("yu gothic ui semibold", 12)))
    foodname_entery.place(x=210, y=200, width=260)
    f_name_line = Canvas(food, width=260, height=1.5, bg="#bdb9b1", highlightthickness=0)
    f_name_line.place(x=210, y=224)

    price = Label(food, text="Price: ", fg="#4f4e4d", font=("yu gothic ui", 13, "bold"))
    price.place(x=100, y=270)
    price_entery = (
        Entry(food, highlightthickness=0, relief=FLAT, bg="white", fg="#6b6a69", font=("yu gothic ui semibold", 12)))
    price_entery.place(x=210, y=270, width=260)
    price_line = Canvas(food, width=260, height=1.5, bg="#bdb9b1", highlightthickness=0)
    price_line.place(x=210, y=294)

    Categorie = Label(food, text="Categories:", fg="#4f4e4d", font=("yu gothic ui", 13, "bold"))
    Categorie.place(x=100, y=350)
    Categorie_comobox = ttk.Combobox(food, foreground="#6b6a69", background="white",
                                     font=("yu gothic ui semibold", 12),
                                     values=["", "Food","Beaverages"])
    Categorie_comobox.place(x=210, y=350)
    Categorie_line = Canvas(food, width=200, height=1.5, bg="#bdb9b1", highlightthickness=0)
    Categorie_line.place(x=210, y=375)

    add = Button(food, text="  ADD  ", width=5, bd=0, bg='#E88B8B', activebackground="#fff", cursor='hand2',
                 fg="#4f4e4d", font=("yu gothic ui", 22, "bold"), command=save)
    add.place(x=100, y=470, height=60)
    up = Button(food, text="  Update  ", width=7, bd=0, bg='#E88B8B', activebackground="#fff", cursor='hand2',
                fg="#4f4e4d", font=("yu gothic ui", 22, "bold"), command= update)
    up.place(x=260, y=470, height=60)
    delete = Button(food, text="  Delete  ", width=6, bd=0, bg='#E88B8B', activebackground="#fff", cursor='hand2',
                    fg="#4f4e4d", font=("yu gothic ui", 22, "bold"), command=delete)
    delete.place(x=450, y=470, height=60)

    food.pack(fill=tk.BOTH, expand=True)


def loginopen():
    import login


def Logout_page():
    Logout_frame = tk.Frame(main_frame)
    sure = messagebox.askyesno("Exit", "Are you sure to LogOut?", parent=window)
    if sure == True:
        window.destroy()
        loginopen()


# Set the protocol for closing the window
window.protocol("logout", Logout_page)

window.geometry("1520x790+0+0")
window.title("Food Delivery Management")
window.resizable(0, 0)
window.configure(bg="#fff")

frame = Frame(window, width=260, height=777, bg="#434343")
frame.place(x=0, y=5)

frame2 = Frame(window, width=1250, height=60, bg="#0066FF")
frame2.place(x=261, y=5)
# enter = Entry(window,width=35,bg="red")

main_frame = tk.Frame(window, highlightbackground='black', highlightthickness=0)
main_frame.place(x=261, y=68)
main_frame.pack_propagate(False)
main_frame.configure(height=712, width=1250)

#home page called
home_page()

enter = (Entry(window, width=30, font=('Bell MT', 15, 'bold'), fg="#000"
               , cursor='hand2'))

enter.place(x=350, y=20)
enter.insert(0, 'Search...')
enter.bind('<FocusIn>', search_enter)

searching = PhotoImage(file='search2.png')
sci = Button(window, image=searching, command=search, bd=0, bg="#0066FF", activebackground="#0066FF", cursor='hand2')
sci.place(x=690, y=20)

# icon = PhotoImage(file='Starbucks-removebg.png')
# logo = tk.Label(window, image=icon, bd=0, cursor='hand2')
# logo.place(x=0, y=15)

# picolumen = PhotoImage(file='list.png')
# menu = tk.Label(window, image=picolumen, cursor='hand2', bg="#0066FF")
# menu.place(x=270, y=20)

# Shut = PhotoImage(file='shutswonimg.png')
# shutlogo = tk.Button(window, image=Shut, bd=0, bg="#434343", cursor='hand2', activebackground="#434343",
#                      command=shutdown)
# shutlogo.place(x=1, y=650)

shut = Button(window, text="ShutDown", font=('Bell MT', 23, 'bold'), bd=0, activebackground="#434343", bg="#434343"
              , cursor='hand2', fg="#b1a4a5", command=shutdown)
shut.place(x=50, y=650)
b0 = Button(window, text="Home", font=('Californian FB', 20), bd=0, activebackground="#434343", bg="#434343"
            , cursor='hand2', fg="#b1a4a5", command=lambda: indicate(b0_indicate, home_page))
b0.place(x=50, y=190)
b0_indicate = tk.Label(window, text='', bg="#434343")
b0_indicate.place(x=50, y=235, width=140, height=5)
# home = PhotoImage(file='3d-house.png')
# homeicon = tk.Button(window, image=home, bd=0, bg="#434343", cursor='hand2', activebackground="#434343")
# homeicon.place(x=5, y=190)

b1 = Button(window, text="Employee", font=('Californian FB', 20), bd=0, activebackground="#434343", bg="#434343"
            , cursor='hand2', fg="#b1a4a5", command=lambda: indicate(b1_indicate, employee))
b1.place(x=50, y=260)
b1_indicate = tk.Label(window, text='', bg="#434343")
b1_indicate.place(x=50, y=310, width=140, height=5)
# emp = PhotoImage(file='add-group.png')
b1icon = tk.Button(window, text='add', bd=0, bg="#434343", cursor='hand2', activebackground="#434343")
b1icon.place(x=5, y=260)

b2 = Button(window, text="Manager", font=('Californian FB', 20), bd=0, activebackground="#434343", bg="#434343"
            , cursor='hand2', fg="#b1a4a5", command=lambda: indicate(b2_indicate, list))
b2.place(x=50, y=330)
b2_indicate = tk.Label(window, text='', bg="#434343")
b2_indicate.place(x=50, y=380, width=150, height=5)
# manage = PhotoImage(file='manager.png')
b2icon = tk.Button(window, text='manager', bd=0, bg="#434343", cursor='hand2', activebackground="#434343")
b2icon.place(x=5, y=330)

b3 = Button(window, text="Delivery Boy", font=('Californian FB', 20), bd=0, activebackground="#434343", bg="#434343"
            , cursor='hand2', fg="#b1a4a5", command=lambda: indicate(b3_indicate, Dellivery_boy))
b3.place(x=50, y=400)
b3_indicate = tk.Label(window, text='', bg="#434343")
b3_indicate.place(x=50, y=450, width=150, height=5)
# deliv = PhotoImage(file='delivery-man.png')
b3icon = tk.Button(window, text='d', bd=0, bg="#434343", cursor='hand2', activebackground="#434343")
b3icon.place(x=5, y=400)

b4 = Button(window, text="Food", font=('Californian FB', 20), bd=0, activebackground="#434343", bg="#434343"
            , cursor='hand2', fg="#b1a4a5", command=lambda: indicate(b4_indicate, addfood))
b4.place(x=50, y=470)
b4_indicate = tk.Label(window, text='', bg="#434343")
b4_indicate.place(x=50, y=520, width=150, height=5)
# addf = PhotoImage(file='dish.png')
# b4icon = tk.Button(window, image=addf, bd=0, bg="#434343", cursor='hand2', activebackground="#434343")
# b4icon.place(x=5, y=470)

b6 = Button(window, text="Logout", font=('Californian FB', 20), bd=0, activebackground="#434343", bg="#434343"
            , cursor='hand2', fg="#b1a4a5", command=lambda: indicate(b6_indicate, Logout_page))
b6.place(x=50, y=550)
b6_indicate = tk.Label(window, text='', bg="#434343")
b6_indicate.place(x=50, y=595, width=100, height=5)
# log = PhotoImage(file='check-out.png')
b6icon = tk.Button(window, text='log', bd=0, bg="#434343", cursor='hand2', activebackground="#434343")
b6icon.place(x=5, y=550)

window.mainloop()
