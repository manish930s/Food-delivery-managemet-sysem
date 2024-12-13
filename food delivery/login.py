import tkinter as tk
from tkinter import *
from tkinter import messagebox
import pymysql
from PIL import Image, ImageTk


def homepagee():
    window.destroy()
    import home
def cannect_data():
    if username.get()=='' or passowrdEntry.get()=='' or username.get()=='Username' or passowrdEntry.get()=='Passowrd':
        messagebox.showerror('Error',"All fields are Required")
    elif check.get() == 0:
        messagebox.showerror('Error', 'Please accept Terms')

    else:
        try:
            con = pymysql.connect(host='localhost', user='root', password='Admin@21')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Database Connectivity Issue, Please Try Again')
            return

        query = 'use pythonpro'
        mycursor.execute(query)

        query = 'select * from addemployee where fname = %s and passwordd = %s'
        mycursor.execute(query,(username.get(), passowrdEntry.get()))

        row = mycursor.fetchone()
        if row is None:
            messagebox.showerror('Error', 'Invalid username or Password')
        else:
            messagebox.showinfo('Welcome', 'Login is Successful')
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
    if username.get()=='Username':
        username.delete(0,END)
def pss_enter(eventt):
    if passowrdEntry.get()=='Password':
        passowrdEntry.delete(0,END)

window = tk.Tk()
window.geometry("1060x650+190+80")
window.title("Food Delivery Managemant")
window.resizable(0,0)
# window.configure(bg="#CCCCCC")

# photo = PhotoImage(file="logoo.png")
# img_label = tk.Label(window, image=photo)
# img_label.place(x=10, y=30)

frame = Frame(window,width=450,height=640,bg="#0066FF")
frame.place(x=600,y=5)

heading = Label(window,text='LOGIN',font=('Bell MT',23,'bold'),bg="#0066FF",fg="white").place(x=780,y=70)

username= (Entry(window,width=16,font=('Bell MT',15,'bold'),fg="#CBCAC5"
                    ,bd=0,bg="#0066FF",cursor='hand2'))
username.place(x=690,y=150)
username.insert(0,'Username')
username.bind('<FocusIn>',user_enter)

fraem1=Frame(window,width=250,height=2)
fraem1.place(x=690,y=190)

passowrdEntry= (Entry(window,width=16,font=('Bell MT',15,'bold'),fg="#CBCAC5"
                    ,bd=0,bg="#0066FF",cursor='hand2'))
passowrdEntry.place(x=690,y=240)
passowrdEntry.insert(0,'Password')
passowrdEntry.bind('<FocusIn>',pss_enter)

fraem2=Frame(window,width=250,height=2)
fraem2.place(x=690,y=280)

# openeye = PhotoImage(file='open_eyeicon.png')
# openeyeButton = Button(window, image=openeye, bd=0, bg="#0066FF", activebackground="#0066FF", cursor='hand2', command=hide)
# openeyeButton.place(x=900, y=240)



check =IntVar()
terms= Checkbutton(window,text='I agree to the Terms & Con*',font=('Bell MT',16),bg="#0066FF",
                   activebackground="#0066FF", cursor='hand2',variable=check)
terms.place(x=670,y=310)

# login = PhotoImage(file='loginbutton 1.png')  # Adjusted file name
loginButton = Button(window, bd=0,text='login', bg="#0066FF", activebackground="#0066FF",
                     command=cannect_data, cursor='hand2')
loginButton.place(x=720, y=390)


fraem3=Frame(window,width=450,height=2)
fraem3.place(x=600,y=530)

text = Label(window,text='Are you admin ? ',font=('Bell MT',16),bg="#0066FF",fg="white").place(x=700,y=580)
adminnbutton = Button(window,text='Admin login',bd=0,bg="#0066FF",activebackground="#0066FF",
                      command=admin_login,cursor='hand2',font=('Bell MT',16),fg='#050aae')
adminnbutton.place(x=850, y=580)

window.mainloop()