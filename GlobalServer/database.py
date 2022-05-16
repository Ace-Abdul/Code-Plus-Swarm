"""
Created on Tue Jul  6 2021

@author: Ace Abdulrahman
"""

import sqlite3 as sq
import secrets
import datetime
import hashlib

def adminDB():
    try:
        with sq.connect("global.db") as db:          
            crsr= db.cursor()
            crsr.execute("""CREATE TABLE admins (
                email TEXT,
                description TEXT,
                dateAdded TEXT,
                password TEXT)""")
            addAdmin('admin','Head Admin','Homenetwork_21')
                
    except sq.OperationalError:
        pass

def toHash(pwd):
    ret = hashlib.sha256(pwd.encode()).hexdigest()
    return ret

def addAdmin(email, desc, password):
    with sq.connect("global.db") as db:          
            crsr= db.cursor()
            pwd = toHash(password)
            today = datetime.date.today()            #Current date
            crntDate = today.strftime('%m-%d-%y')    #Format date correctly mm/dd/yy
            crsr.execute("INSERT INTO admins VALUES (?,?,?,?)", (email, desc, crntDate, pwd))


def isPwd(username, pwd):                             #Checks if password exists in db
    with sq.connect("global.db") as db:
        crsr= db.cursor()
        hashed = toHash(pwd)
        notNull = crsr.execute("SELECT * FROM admins WHERE password = (?) AND email=(?)", (hashed, username) ).fetchone()
        if notNull:
            #print("exists")
            return True
        else:
            #print("existsn't")
            return False

def showAdmins():
    with sq.connect("global.db") as db:
        crsr= db.cursor()
        crsr.execute("SELECT rowid, * FROM admins")
        x= crsr.fetchall()
        return x


def delAdmin(row):
    with sq.connect("global.db") as db:
        crsr= db.cursor()
        crsr.execute("DELETE FROM admins WHERE rowid = (?)", (row,))

def updateAdmin(email, desc, date, rowid):
    with sq.connect("global.db") as db:
        crsr= db.cursor()
        #pwd= toHash(pwd)
        crsr.execute("UPDATE admins SET email = (?), Description = (?), dateAdded = (?) WHERE rowid=(?)", (email, desc, date, rowid))

def changePwd(newPwd, user):
     with sq.connect("global.db") as db:
        crsr= db.cursor()
        pwd = toHash(newPwd)
        crsr.execute("UPDATE admins SET password = (?) WHERE email = (?)", (pwd, user))

def createDB():
    try:
        db = sq.connect("global.db")                #Connects to database (db) file
        crsr = db.cursor()                          #cursor used to edit db file     
        crsr.execute("""CREATE TABLE users (         
                            email TEXT,
                            Description TEXT,
                            dateAdded TEXT,
                            token TEXT)""")   #Creates table w/ token, email, date added, and description as columns
        db.commit()
        db.close()                                  #Commit changes and close file
    except sq.OperationalError:
        pass
            
def genToken(email, description):
    #email = input("Enter email: ")              
    token = (secrets.token_hex())               #Generate random token
    #description = input("Describe the user who is being added: ")
    createDB()
    addToken(token, email, description)         

def addToken(token, email, description):
    with sq.connect("global.db") as db:          
        crsr= db.cursor()
        today = datetime.date.today()            #Current date
        crntDate = today.strftime('%m-%d-%y')    #Format date correctly mm/dd/yy
        crsr.execute("INSERT INTO users VALUES (?, ?, ?, ?)",(email, description, crntDate, token))  # Adding user info into db  
        crsr.execute("SELECT * FROM users")      # Select all (*) rows from table
        x= crsr.fetchall()                       # Grab all rows and pass in to x variable
        #print(x)
        return x

def isToken(token):                             #Checks if token exists in db
    with sq.connect("global.db") as db:
        crsr= db.cursor()
        if (crsr.execute("SELECT * FROM users WHERE token = (?)", (token,) ).fetchall()):
            #print("exists")
            return True
        else:
            #print("existsn't")
            return False

def findToken(email):
    with sq.connect("global.db") as db:
        crsr= db.cursor()
        crsr.execute("SELECT token FROM users WHERE email = (?)", (email,))
        x = crsr.fetchall()

    return x

def showTokens():                               #Displays rows in table without headers
    with sq.connect("global.db") as db:
        crsr= db.cursor()
        crsr.execute("SELECT rowid, * FROM users")
        x= crsr.fetchall()
        #print(x)
    return x

def clearTable():
    with sq.connect("global.db") as db:
        crsr= db.cursor()
        crsr.execute("DELETE FROM users")

def updateTable(email, desc, date, token, rowid):
    with sq.connect("global.db") as db:
        crsr= db.cursor()
        crsr.execute("UPDATE users SET email = (?), Description = (?), dateAdded = (?), token = (?) WHERE rowid=(?)", (email, desc, date, token, rowid))

def deleteUser(row):
    with sq.connect("global.db") as db:
        crsr= db.cursor()
        crsr.execute("DELETE FROM users WHERE rowid = (?)", (row,))


