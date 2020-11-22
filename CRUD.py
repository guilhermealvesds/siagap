from tkinter.ttk import *
from tkinter import *
import sqlite3
from tkinter import messagebox
con = sqlite3.connect('banco.db')
mycursor=con.cursor()
#Criar tabela clientes
mycursor.execute("""CREATE TABLE IF NOT EXISTS student (
            RollNo VARCHAR PRIMARY KEY,
            First_Name VARCHAR,
            Last_Name VARCHAR,
            Phone_Number VARCHAR,
            City VARCHAR,            
            State VARCHAR,
            Age VARCHAR)""")
root=Tk()
root.title("Student Data")
root.geometry("1200x700")
#photo=PhotoImage(file='image.png')
#label12=Label(root,image=photo).grid(row=8,column=5)
label1=Label(root,text="RollNo",width=20,height=2,bg="pink").grid(row=0,column=0)
label2=Label(root,text="First_Name",width=20,height=2,bg="pink").grid(row=1,column=0)
label3=Label(root,text="Last_Name",width=20,height=2,bg="pink").grid(row=2,column=0)
label4=Label(root,text="Phone_Number",width=20,height=2,bg="pink").grid(row=3,column=0)
label5=Label(root,text="City",width=20,height=2,bg="pink").grid(row=4,column=0)
label6=Label(root,text="State",width=20,height=2,bg="pink").grid(row=5,column=0)
label7=Label(root,text="Age",width=20,height=2,bg="pink").grid(row=6,column=0)
label8=Label(root,width=10,height=2).grid(row=7,column=2)
label9=Label(root,width=10,height=2).grid(row=7,column=4)
label10=Label(root,width=10,height=2).grid(row=7,column=6)
label11=Label(root,width=10,height=2).grid(row=7,column=8)
e1=Entry(root,width=30,borderwidth=8)
e1.grid(row=0,column=1)
e2=Entry(root,width=30,borderwidth=8)
e2.grid(row=1,column=1)
e3=Entry(root,width=30,borderwidth=8)
e3.grid(row=2,column=1)
e4=Entry(root,width=30,borderwidth=8)
e4.grid(row=3,column=1)
e5=Entry(root,width=30,borderwidth=8)
e5.grid(row=4,column=1)
e6=Entry(root,width=30,borderwidth=8)
e6.grid(row=5,column=1)
e7=Entry(root,width=30,borderwidth=8)
e7.grid(row=6,column=1)
def Register():
    RollNo=e1.get()
    dbRollNo=""
    Select="select RollNo from student where RollNo='%s'" %(RollNo)
    mycursor.execute(Select)
    result=mycursor.fetchall()
    for i in result:
        dbRollNo=i[0]
    if(RollNo == dbRollNo):
        messagebox.askokcancel("Information","Record Already exists")
    else:
        Insert=''' Insert into student(RollNo,First_Name,Last_Name,Phone_Number,City,State,Age) values(?,?,?,?,?,?,?) '''
        First_Name=e2.get()
        Last_Name=e3.get()
        Phone_Number=e4.get()
        City=e5.get()
        State=e6.get()
        Age=e7.get()
        if(First_Name !="" and Last_Name !="" and Phone_Number !="" and City !="" and State !="" and Age !=""):
            Value=(RollNo,First_Name,Last_Name,Phone_Number,City,State,Age)
            mycursor.execute(Insert,Value)
            con.commit()
            messagebox.askokcancel("Information","Record inserted")
            e1.delete(0, END)
            e2.delete(0, END)
            e3.delete(0, END)
            e4.delete(0, END)
            e5.delete(0, END)
            e6.delete(0, END)
            e7.delete(0, END)
        else:
            if (First_Name == "" and Last_Name == "" and Phone_Number == "" and City == "" and State == "" and Age == ""):
             messagebox.askokcancel("Information","New Entery Fill All Details")
            else:
             messagebox.askokcancel("Information", "Some fields left blank")
def ShowRecord():
    RollNo=e1.get()
    dbRollNo=""
    Select="select RollNo from student where RollNo='%s'" %(RollNo)
    mycursor.execute(Select)
    result1=mycursor.fetchall()
    for i in result1:
        dbRollNo=i[0]
    Select1="select First_Name,Last_Name,Phone_Number,City,State,Age from student where RollNo='%s'" %(RollNo)
    mycursor.execute(Select1)
    result2=mycursor.fetchall()
    First_Name=""
    Last_Name=""
    Phone_Number=""
    City=""
    State=""
    Age=""
    if(RollNo == dbRollNo):
        for i in result2:
            First_Name=i[0]
            Last_Name=i[1]
            Phone_Number=i[2]
            City=i[3]
            State=i[4]
            Age=i[5]
        e2.insert(0,First_Name)
        e3.insert(0, Last_Name)
        e4.insert(0, Phone_Number)
        e5.insert(0, City)
        e6.insert(0, State)
        e7.insert(0, Age)
    else:
        messagebox.askokcancel("Information","No Record exists")
def Delete():
    RollNo=e1.get()
    Delete="delete from student where RollNo='%s'" %(RollNo)
    mycursor.execute(Delete)
    con.commit()
    messagebox.showinfo("Information","Record Deleted")
    e1.delete(0,END)
    e2.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)
    e5.delete(0, END)
    e6.delete(0, END)
    e7.delete(0,END)
def Update():
    RollNo=e1.get()
    First_Name=e2.get()
    Last_Name=e3.get()
    Phone_Number=e4.get()
    City=e5.get()
    State=e6.get()
    Age=e7.get()
    Update="Update student set First_Name='%s', Last_Name='%s', Phone_Number='%s', City='%s', State='%s', Age='%s' where RollNo='%s'" %(First_Name,Last_Name,Phone_Number,City,State,Age,RollNo)
    mycursor.execute(Update)
    con.commit()
    messagebox.showinfo("Info","Record Update")
def Showall():
    class A(Frame):
        def __init__(self, parent):
            Frame.__init__(self, parent)
            self.CreateUI()
            self.LoadTable()
            self.grid(sticky=(N, S, W, E))
            parent.grid_rowconfigure(0, weight=1)
            parent.grid_columnconfigure(0, weight=1)
        def CreateUI(self):
            tv= Treeview(self)
            tv['columns']=('RollNo', 'First_Name', 'Last_Name', 'Phone_Number', 'City', 'State', 'Age')
            tv.heading('#0',text='RollNo',anchor='center')
            tv.column('#0',anchor='center')
            tv.heading('#1', text='First_Name', anchor='center')
            tv.column('#1', anchor='center')
            tv.heading('#2', text='Last_Name', anchor='center')
            tv.column('#2', anchor='center')
            tv.heading('#3', text='Phone_Number', anchor='center')
            tv.column('#3', anchor='center')
            tv.heading('#4', text='City', anchor='center')
            tv.column('#4', anchor='center')
            tv.heading('#5', text='State', anchor='center')
            tv.column('#5', anchor='center')
            tv.heading('#6', text='Age', anchor='center')
            tv.column('#6', anchor='center')
            tv.grid(sticky=(N,S,W,E))
            self.treeview = tv
            self.grid_rowconfigure(0,weight=1)
            self.grid_columnconfigure(0,weight=1)
        def LoadTable(self):
            Select="Select * from student"
            mycursor.execute(Select)
            result=mycursor.fetchall()
            RollNo=""
            First_Name=""
            Last_Name=""
            Phone_Number=""
            City=""
            State=""
            Age=""
            for i in result:
                RollNo=i[0]
                First_Name=i[1]
                Last_Name=i[2]
                Phone_Number=i[3]
                City=i[4]
                State=i[5]
                Age=i[6]
                self.treeview.insert("",'end',text=RollNo,values=(First_Name,Last_Name,Phone_Number,City,State,Age))
    root=Tk()
    root.title("Overview Page")
    A(root)
def Clear():
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)
    e5.delete(0, END)
    e6.delete(0, END)
    e7.delete(0, END)
button1=Button(root,text="Register",width=10,height=2,command=Register).grid(row=7,column=0)
button2=Button(root,text="Delete",width=10,height=2,command=Delete).grid(row=7,column=1)
button3=Button(root,text="Update",width=10,height=2,command=Update).grid(row=7,column=3)
button4=Button(root,text="Show record",width=10,height=2,command=ShowRecord).grid(row=7,column=5)
button5=Button(root,text="Show All",width=10,height=2,command=Showall).grid(row=7,column=7)
button6=Button(root,text="Clear",width=10,height=2,command=Clear).grid(row=7,column=9)
root.mainloop()
