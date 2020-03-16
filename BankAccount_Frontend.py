from tkinter import *
from Bank_Account_Backend import queries
import re
import pandas as pd
"""
Fields: FirstName, LastName, Address, PostCode,
AccountNumber,Balance,PayInAmount,WithdrawalAmount
"""
countriesFile = pd.read_excel('international-dialing-country-codes.xlsx')
countriesData = countriesFile[['Country','Dial Code']]
query_var=queries("TestDb.db")
idx=None
current_balance=None
def get_current_row(event):
    global idx
    global current_balance
    try:
        record_position=main_display.curselection()[0]
        record_tuple=main_display.get(record_position)
        #print(type(record_tuple[0]))
        idx = record_tuple[0]
        current_balance=record_tuple[3]        
        lname_entry.delete(0,END)
        lname_entry.insert(END,record_tuple[1])
        fname_entry.delete(0,END)
        fname_entry.insert(END,record_tuple[2])
        balance_entry.delete(0,END)
        balance_entry.insert(END,record_tuple[3])
        pcode_entry.delete(0,END)
        pcode_entry.insert(END,record_tuple[4])
        address_entry.delete(0,END)
        address_entry.insert(END,record_tuple[5])
        country_value.set(record_tuple[6])        
        mobile_entry.delete(0,END)
        mobile_entry.insert(END,record_tuple[7])
        email_entry.delete(0,END)
        email_entry.insert(END,record_tuple[8])        
        accNum=query_var.getAccountNum(idx)
        account_entry.delete(0,END)
        account_entry.insert(END,accNum)
        callSelectTransaction()
        callGetDialCode()             
    except IndexError:
        print("No record is selected!")      

def callSelectAll():
    main_display.delete(0,END)
    allCustomers=query_var.selectAll()
    for x in allCustomers:
        main_display.insert(END,x)    

def callSelectTransaction():    
    transaction_display.delete(0,END)
    results=query_var.selectTransactions(idx)    
    for x in results:        
        transaction_display.insert(END,x)

def callSearch():
    main_display.delete(0,END)
    searcResult=query_var.searchCustomer(lname_value.get(),fname_value.get(),pcode_value.get(),address_value.get())
    for x in searcResult:
        main_display.insert(END,x)

def callAddCustomer():   
    query_var.insertCustomer(lname_value.get(),fname_value.get(),0,
    pcode_value.get(),address_value.get(),str(country_value.get()),dialCode_value.get(),mobile_value.get(),email_value.get()) 

def callUpdateCustomer():    
    query_var.updateCustomer(idx,lname_value.get(),fname_value.get(),pcode_value.get(),
    address_value.get(),country_value.get(),dialCode_value.get(),mobile_value.get(),email_value.get())    

def callPayIn():
    query_var.payin(idx,balance_value.get(),payin_value.get(),lname_value.get(),fname_value.get())    

def callWithdrawal():   
    query_var.withdrawal(idx,balance_value.get(),withdraw_value.get(),lname_value.get(),fname_value.get())    
    
def callDeleteCustomer():
    confrimDelWindow=Toplevel()
    confirmDelLabel=Label(confrimDelWindow,width=30,text="Please Confirm delete or cancel")
    confirmDelLabel.grid(row=0,column=1)
    confirmButton=Button(confrimDelWindow,text="Yes",command=deleteConfirmed)
    confirmButton.grid(row=1,column=0,sticky=E,columnspan=1)
    cancelButton=Button(confrimDelWindow,text="Cancel",command=confrimDelWindow.destroy)
    cancelButton.grid(row=1,column=1,sticky=W,columnspan=1)
def deleteConfirmed():
    toDelete=lname_value.get()+" "+fname_value.get()
    query_var.deleteWithdrawal(idx,balance_value.get(),float(balance_value.get()))
    finalBalance=balance_value.get()
    query_var.deleteCustomer(idx)
    print(toDelete+" has been deleted and their final balance of "+finalBalance+" transfered!")

def callGetDialCode(*args):
    #country_drop.
    dialCode=query_var.getDialCode(str(country_value.get()))
    try:
        dialCode_box.delete(0,END)
        dialCode_box.insert(END,dialCode)
    except:
        dialCode_box.delete(0,END)
        dialCode_box.insert(END,"00")
    

BankAccount_Window = Tk()
BankAccount_Window.wm_title("Olatunji Bank Plc")

lname_label = Label(BankAccount_Window,width=12,text="Last Name")
lname_label.grid(row=0,column=0)
lname_value = StringVar()
lname_entry=Entry(BankAccount_Window,width=20,textvariable=lname_value)
lname_entry.grid(row=0,column=1)

fname_label = Label(BankAccount_Window,width=12,text="First Name")
fname_label.grid(row=0,column=2)
fname_value = StringVar()
fname_entry = Entry(BankAccount_Window,width=20,textvariable=fname_value)
fname_entry.grid(row=0,column=3)

email_label = Label(BankAccount_Window,width=12,text="Email")
email_label.grid(row=0,column=4)
email_value=StringVar()
email_entry=Entry(BankAccount_Window,width=20,textvariable=email_value)
email_entry.grid(row=0,column=5)

address_label = Label(BankAccount_Window,width=12,text="Address")
address_label.grid(row=0,column=6)
address_value = StringVar()
address_entry=Entry(BankAccount_Window,width=40,textvariable=address_value)
address_entry.grid(row=0,column=7,sticky=E,columnspan=3)

mobile_label = Label(BankAccount_Window,width=12,text="Mobile")
mobile_label.grid(row=1,column=1)
dialCode_value=StringVar()
dialCode_box=Entry(BankAccount_Window,width=6,textvariable=dialCode_value)
dialCode_box.grid(row=1,column=2)
mobile_value = StringVar()
mobile_entry = Entry(BankAccount_Window,width=20,textvariable=mobile_value)
mobile_entry.grid(row=1,column=3)

#Country here
country_value=StringVar(BankAccount_Window)
country_value.set('Choose Country')
country_drop = OptionMenu(BankAccount_Window,country_value,*countriesData['Country'],command=callGetDialCode)
country_drop.config(width=30,font=('Calibri', 12))
country_drop.grid(row=1,column=0,sticky=(N,W,E,S))
#country_drop.bind("<Button-1>",callGetDialCode)

pcode_label = Label(BankAccount_Window,width=12,text="Post Code")
pcode_label.grid(row=1,column=4)
pcode_value=StringVar()
pcode_entry=Entry(BankAccount_Window,width=20,textvariable=pcode_value)
pcode_entry.grid(row=1,column=5)

balance_label = Label(BankAccount_Window,width=12,text="Balance")
balance_label.grid(row=23,column=7,sticky=E)
balance_value = StringVar()
balance_entry=Entry(BankAccount_Window,width=20,textvariable=balance_value)
balance_entry.grid(row=23,column=8)

account_label = Label(BankAccount_Window,width=12,text="Account No:")
account_label.grid(row=24,column=7,sticky=E)
account_value = StringVar()
account_entry=Entry(BankAccount_Window,width=20,textvariable=account_value)
account_entry.grid(row=24,column=8)

info_label = Label(BankAccount_Window,width=15,text="Withdraw/Pay in:")
info_label.grid(row=1,column=6)

payin_button=Button(BankAccount_Window,width=20,text="<--Pay in",command=callPayIn)
payin_button.grid(row=1,column=8)
payin_value=StringVar()
payin_entry=Entry(BankAccount_Window,width=20,textvariable=payin_value)
payin_entry.grid(row=1,column=7)

withdraw_button=Button(BankAccount_Window,width=20,text="<--Withdraw",command=callWithdrawal)
withdraw_button.grid(row=2,column=8)
withdraw_value=StringVar()
withdraw_entry=Entry(BankAccount_Window,width=20,textvariable=withdraw_value)
withdraw_entry.grid(row=2,column=7)

viewAll_button=Button(BankAccount_Window,text="View All",width=20,command=callSelectAll)
viewAll_button.grid(row=3,column=8)

search_button=Button(BankAccount_Window,text="Search Entry",width=20,command=callSearch)
search_button.grid(row=4,column=8)

addEntry_button=Button(BankAccount_Window,text="Add Entry",width=20,command=callAddCustomer)
addEntry_button.grid(row=5,column=8)

update_button=Button(BankAccount_Window,text="Update Selected",width=20,command=callUpdateCustomer)
update_button.grid(row=6,column=8)

delete_button=Button(BankAccount_Window,text="Delete Selected",width=20,command=callDeleteCustomer)
delete_button.grid(row=7,column=8)

close_button=Button(BankAccount_Window,text="Close",width=20,command=BankAccount_Window.destroy)
close_button.grid(row=8,column=8)

#Main Display
main_label=Label(BankAccount_Window,width=30,text="Customer Information")
main_label.grid(row=3,column=0,sticky=W,columnspan=1)
main_display = Listbox(BankAccount_Window,width=80,height=10)
main_display.grid(row=4,column=0,rowspan=10,columnspan=4,sticky=W)

main_scroll=Scrollbar(BankAccount_Window)
main_scroll.grid(row=6,column=3)
#Configure listboy and main_display
main_display.configure(yscrollcommand=main_scroll.set)
main_scroll.configure(command=main_display.yview)
#select action in main_display
main_display.bind('<<ListboxSelect>>',get_current_row)

#Transactions view
transaction_label=Label(BankAccount_Window,width=30,text="Transactions")
transaction_label.grid(row=19,column=0,sticky=W,columnspan=1)
transaction_display=Listbox(BankAccount_Window,width=60,height=6)
transaction_display.grid(row=20,column=0,rowspan=6,columnspan=3,sticky=W)

transaction_scroll=Scrollbar(BankAccount_Window)
transaction_scroll.grid(row=23,column=3)
#Configure transaction display and scroll
transaction_display.configure(yscrollcommand=transaction_scroll.set)
transaction_scroll.configure(command=transaction_display.yview)


BankAccount_Window.mainloop()