import tkinter as tk
from tkinter import messagebox
from tkinter import *
import pymysql


# import  pymysql

def homepagee():
    window.destroy()
    import adminloginpage
def connect_database():
    if username.get() == '' or passowrdEntry.get() == '' or EmailEntry.get() == '' or username.get() == 'Adminname' or passowrdEntry.get() == 'Passowrd' or EmailEntry.get() == 'Email':
        messagebox.showerror('Error', 'All fields are Required')
    elif check.get()==0:
        messagebox.showerror('Error', 'Please accept Terms')
    else:
        con = pymysql.connect(host='localhost', user='root', password='Admin@21', database='pythonpro')
        mycursor = con.cursor()

        query = 'select * from adminlogin where email = %s and adminname = %s'
        mycursor.execute(query,(EmailEntry.get(),username.get()))
        row = mycursor.fetchone()
        if row is None:
            messagebox.showerror('Error', 'Incorrect username or Email ID')
        else:
            query='update adminlogin set password = %s where adminname = %s and email = %s'
            mycursor.execute(query,(passowrdEntry.get(),username.get(),EmailEntry.get()))
            con.commit()
            con.close()
            messagebox.showinfo('Success', 'Password is reset , Please login with new Password')

            homepagee()

def admin_login():
    window.destroy()
    import adminloginpage


def hide():
    openeye.config(file='eye.png')
    passowrdEntry.config(show='*')
    openeyeButton.config(command=show)


def show():
    openeye.config(file='open_eyeicon.png')
    passowrdEntry.config(show='')
    openeyeButton.config(command=hide)


def user_enter(event):
    if username.get() == 'Adminname':
        username.delete(0, END)


def pss_enter(eventt):
    if passowrdEntry.get() == 'New Passowrd':
        passowrdEntry.delete(0, END)


def email_enter(event):
    if EmailEntry.get() == 'Email':
        EmailEntry.delete(0, END)


window = tk.Tk()

window.geometry("1060x650+190+80")
window.title("Food Delivery Managemant")
window.resizable(0, 0)
window.configure(bg="#fff")

# def staff_login():
photo = PhotoImage(file="adminnn2.png")

img_label = tk.Label(
    window,
    image=photo,
    bg="#fff"
).place(x=0, y=50)
frame = Frame(window, width=450, height=640, bg="#fff")
frame.place(x=600, y=5)

heading = Label(window, text='ADMIN FORGOT PASSWORD', font=('Bell MT', 23, 'bold'), bg="#fff").place(x=600, y=50)

username = (Entry(window, width=16, font=('Bell MT', 15, 'bold'), bd=0,fg="#6b6a69", cursor='hand2'))
username.place(x=690, y=140)
username.insert(0, 'Adminname')
username.bind('<FocusIn>', user_enter)

fraem1 = Frame(window, width=250, height=2, bg="#75eceb")
fraem1.place(x=690, y=180)

passowrdEntry = (Entry(window, width=16, font=('Bell MT', 15, 'bold'), fg="#6b6a69",bd=0, cursor='hand2'))
passowrdEntry.place(x=690, y=230)
passowrdEntry.insert(0, 'New Passowrd')
passowrdEntry.bind('<FocusIn>', pss_enter)

fraem2 = Frame(window, width=250, height=2, bg="#75eceb")
fraem2.place(x=690, y=270)

EmailEntry = (Entry(window, width=16, font=('Bell MT', 15, 'bold'),fg="#6b6a69", bd=0, cursor='hand2'))
EmailEntry.place(x=690, y=310)
EmailEntry.insert(0, 'Email')
EmailEntry.bind('<FocusIn>', email_enter)

fraem3 = Frame(window, width=250, height=2, bg="#75eceb")
fraem3.place(x=690, y=360)

openeye = PhotoImage(file='open_eyeicon.png')
openeyeButton = Button(window, image=openeye, bd=0, bg="#fff", activebackground="#fff", cursor='hand2', command=hide)
openeyeButton.place(x=900, y=230)

check =IntVar()
terms = Checkbutton(window, text='I agree to the Terms', font=('Bell MT', 16),fg="#6b6a69", bg="#fff",
                    activebackground="#fff", cursor='hand2',variable=check)
terms.place(x=670, y=370)

login = PhotoImage(file='looo.png')
loginButton = Button(window, image=login, bd=0, bg="#fff", activebackground="#fff", cursor='hand2',
                     command=connect_database)
loginButton.place(x=680, y=450)

fraem3 = Frame(window, width=450, height=2)
fraem3.place(x=600, y=540)

text = Label(window, text='Move Admin Login ', font=('Bell MT', 16), bg="#fff").place(x=700, y=580)
adminnbutton = Button(window, text='login', bd=0, bg="#fff", activebackground="#fff",
                      command=admin_login, cursor='hand2', font=('Bell MT', 16), fg='#050aae')
adminnbutton.place(x=890, y=575)

window.mainloop()
