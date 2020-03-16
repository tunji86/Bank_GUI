import sqlite3
from datetime import *
import re
import pandas as pd

#selectAll,search,addcustomer,update,delete,payin,withdraw
idArray=[]
class queries:
    
    def __init__(self,db):
        self.connection = sqlite3.connect(db)
        self.myCursor = self.connection.cursor()
        self.myCursor.execute("create table if not exists Customers(Cid integer primary key autoincrement,"
        "LastName text,FirstName text,Balance float,Postcode text,Address text,Country text, Mobile text,Email text,FullNumber text)")
        self.myCursor.execute("create table if not exists Accounts(AccountNum integer primary key autoincrement, Cid integer,foreign key(Cid) references Customers(Cid))")
        self.myCursor.execute("create table if not exists Transactions(Tid integer primary key autoincrement,"
        "Cid integer,Tdate datetime,Amount int,Action Text,foreign key(Cid) references Customers(Cid))")
        self.myCursor.execute("create table if not exists CustomerArchive(Cid integer,LastName text,FirstName text,AccountNum integer,FinalBalance float,Postcode text"
        ",Address text,Country text,Mobile text,Email text)")
        self.myCursor.execute("create table if not exists InfoTable(Country text,DialCode text,PhoneRegex text,PostcodeRegex text)")
        self.connection.commit()    
    
    def setSequence(self):
        count_ = self.myCursor.execute("select * from Accounts").fetchall()
        if len(count_) == 1:
            self.myCursor.execute("UPDATE sqlite_sequence SET seq = 10000 WHERE NAME = 'Accounts'")
            self.myCursor.execute("update Accounts set AccountNum=10000")
        else:
            pass
        self.connection.commit()

    def selectAll(self):       
        return self.myCursor.execute("select * from Customers").fetchall()       

    def insertCustomer(self,lname,fname,balance,pcode,address,country,dialCode,mobile,email):
        if self.verifyEntries(lname,fname,pcode,address,mobile,email,country)==True:
            mobileNum=dialCode+mobile
            self.myCursor.execute("insert into Customers values(null,?,?,?,?,?,?,?,?,?) ",(lname,fname,balance,pcode.upper(),address,country,mobile,email.lower(),mobileNum))                        
            self.insertAccount()                        
            result=self.myCursor.execute("select * from Accounts order by AccountNum desc limit 1").fetchall()
            newAccNum=result[0][0]
            newID=result[0][1]
            self.insertArchive(newID,lname,fname,newAccNum,balance,pcode,address,country,mobileNum,email)
            self.connection.commit()
            print(lname.title()+" "+fname.title()+" has been added!")        


    def insertAccount(self):
        #extract latest customerID
        idExtract=self.myCursor.execute("select max(Cid) from Customers").fetchall()
        newCustID=int(idExtract[0][0])         
        #insert new customer and create account number for them in Accounts
        self.myCursor.execute("insert into Accounts values(null,?) ",(newCustID,))        
        self.connection.commit()
        self.setSequence()        

    def insertArchive(self,cid,lname,fname,accnum,fbalance,pcode,address,country,mobile,email):
        self.myCursor.execute("insert into CustomerArchive values(?,?,?,?,?,?,?,?,?,?)",(cid,lname,fname,accnum,fbalance,pcode,address,country,mobile,email))
    
    def insertTransaction(self,cid,tdate,amount,action):#called by both payin and withdrawal
        self.myCursor.execute("insert into Transactions values(null,?,?,?,?)",(cid,tdate,amount,action))
        self.connection.commit()

    def searchCustomer(self,lname,fname,pcode,address):        
        return self.myCursor.execute("select * from Customers where lower(LastName) like ? and lower(FirstName) like ? and lower(Postcode) like ? and lower(Address) like ?",
        ("%{}%".format(lname),"%{}%".format(fname),"%{}%".format(pcode),"%{}%".format(address))).fetchall()

    def deleteCustomer(self,cid):
        self.myCursor.execute("delete from Customers where Cid = ?",(cid,))
        self.connection.commit()

    def updateCustomer(self,cid,lname,fname,pcode,address,country,dialCode,mobile,email):        
        if self.verifyEntries(lname,fname,pcode,address,mobile,email,country)==True:
            mobileNum=dialCode+mobile
            self.myCursor.execute("update Customers set LastName=?, FirstName=?, Postcode=?, Address=?,Country=?,Mobile=?,Email=?,FullNumber=? where Cid=?",(lname,fname,pcode,address,country,mobile,email,mobileNum,cid))
            self.connection.commit()        
            idArray.append(cid)
            print(lname.title()+" "+fname.title()+" has been upated!")

    def payin(self,cid,currentBalance,amount,lname,fname):
        try:
            newBalance = float(currentBalance) + float(amount)
            self.myCursor.execute("update Customers set Balance=? where Cid=?",(newBalance,cid))
            self.connection.commit()
            self.insertTransaction(cid,datetime.now(),amount,"Credit")
            idArray.append(cid)
            print(amount+" has been credited to "+lname.title()+" "+fname.title()+"'s account!")
        except ValueError:
            print("Please specify amount to pay in!")        

    def withdrawal(self,cid,currentBalance,amount,lname,fname):
        if float(amount) <= float(currentBalance):         
            try:
                newBalance=float(currentBalance)-float(amount)
                self.myCursor.execute("update Customers set Balance=? where Cid=?",(newBalance,cid))
                self.connection.commit()
                self.insertTransaction(cid,datetime.now(),amount,"Debit")
                idArray.append(cid)
                print(amount+" has been debited from "+lname.title()+" "+fname.title()+"'s account!")
            except ValueError:
                print("Please specify a withdrwal amount!")
        else:
            print("You can not withdraw more than "+currentBalance+"!")
    
    def deleteWithdrawal(self,cid,currentBalance,amount):
        newBalance=float(currentBalance)-float(amount)
        self.myCursor.execute("update Customers set Balance=? where Cid=?",(newBalance,cid))
        self.connection.commit()
        self.insertTransaction(cid,datetime.now(),amount,"Debit - Departing")        

    def getAccountNum(self,cid):
        result=self.myCursor.execute("select AccountNum from Accounts where Cid=?",(cid,)).fetchall()
        #print(result[0][0])
        return result[0][0]

    def getDialCode(self,country):
        if country != "Choose Country":
            #result = self.myCursor.execute("select DialCode from InfoTable where Country=?",(country,)).fetchall()[0][0]
            #print(result)             
            try:
                #print(country)
                result = self.myCursor.execute("select DialCode from InfoTable where Country=?",(country,)).fetchall()[0][0]
                #print("Result is "+result)
                return result
            except IndexError:                
                print("No record of "+country+"'s dial code!")
                return None
        

    def selectTransactions(self,cid):        
        return self.myCursor.execute("select * from Transactions where Cid=?",(cid,)).fetchall()
    
    def verifyEmail(self,email_):    
        return (bool(re.search(r'^[A-Z0-9öüä._%+-]+@[A-Z0-9öüä.-]+\.[A-Z]{2,}$',email_,re.IGNORECASE)))

    def verifyName(self,name_):
        return (bool(re.search(r"^[a-zA-Zöüä]+(([',. -][a-zA-Zöüä])?[a-zA-Zöüä]*)*$", name_,re.IGNORECASE)))

    def verifyPhoneNumber(self,country,number_):
        try:
            result = self.myCursor.execute("select PhoneRegex from InfoTable where Country=?",(country,)).fetchall()            
            phoneRegex_=result[0][0]
            return bool(re.search(phoneRegex_, number_))
        except IndexError:
            phoneRegex_="^[1-9]{1}[0-9]{6,10}$"
            return bool(re.search(phoneRegex_, number_))
            print("No record of "+country+"'s phone number format, hence general format is allowed!")
            #return bool(re.search(r"^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]{8,10}$", number_))

    def verifyAddress(self,address_):
        return (bool(re.search(r"^[a-zA-Z0-9üöä]+[',. -]+([a-zA-Z0-9oüä ]?[,'-_ ][a-zA-Z0-9öüä]*)+$", address_,re.IGNORECASE)))

    def extractString(self,string_):
        array_=[]
        for x in range(len(string_)):
            array_.append(string_[x])
        outStr=""
        for x in array_:
            outStr=outStr+x
        return outStr.lower()

    def verifyPostcode(self,country,pcode_):
        print(country)
        try:
            result = self.myCursor.execute("select PostcodeRegex from InfoTable where Country=?",(country,)).fetchall()
            #print(result)
            pcodeRegex_=result[0][0]
            return bool(re.search(pcodeRegex_, pcode_,re.IGNORECASE))
        except IndexError:
            print("No record of "+country+"'s postcode format, hence general format is allowed!")
            return True   
        
        """if bool(re.search("^\d{5}$", pcode_)) or bool(re.search(r"^[A-Za-z]{1,2}[0-9R][0-9A-Za-z]?[ ][0-9][ABD-HJLNP-UW-Z]{2}$", pcode_,re.IGNORECASE)) or bool(re.search("^[0-9]{5}(?:-[0-9]{4})?$", pcode_)):
            return True
        else:
            return False""" 

    def verifyEntries(self,lname,fname,pcode,address,mobile,email,country):
        if self.verifyEmail(email)==False:
            print("Please provide a valid email address")
        elif self.verifyName(fname)==False:
            print("Please provide a valid First name")
        elif self.verifyName(lname)==False:
            print("Please provide a valid Last Name")
        elif self.verifyPhoneNumber(country,mobile)==False:
            print("Please provide a valid "+country+" phone number")
        elif self.verifyAddress(address)==False:
            print("Please provide a valid address")
        elif country=='Choose Country':
            print("Please select your country of residence!")
        elif self.verifyPostcode(country,pcode)==False:
            print("Please provide a valid "+country+" Post or Zip Code")        
        else:
            return True     

    def tetet(self):
        print(self.myCursor.execute("select * from RegexTable where lower(Country)=?",("united kingdom",)).fetchall())


    def __del__(self):        
        for x in set(idArray):
            self.myCursor.execute("delete from CustomerArchive where Cid=?",(x,))
            result=self.myCursor.execute("select * from Customers where Cid=?",(x,)).fetchall()[0]
            self.myCursor.execute("insert into CustomerArchive values(?,?,?,?,?,?,?,?,?,?)",(x,result[1],result[2],0,result[3],result[4],result[5],result[6],result[7],result[8]))
            #(lname,fname,balance,pcode.upper(),address,country,mobile,email))       
            self.myCursor.execute("update CustomerArchive set AccountNum=(Select AccountNum from Accounts where Cid=?) where Cid=?",(x,x))
        self.connection.commit()          
        print("Connection closed!!!")
        self.connection.close()

#qq=queries("TestDb.db")
#country__='Germany'
#qq.getDialCode(country__)


#query_var=queries
#query_var("TestDb.db").selectAll()
#query_var("TestDb.db")
#query_var("TestDb.db").insertCustomer("Thane","Micha",0,"39104","Alle Centre, Lane 4")
