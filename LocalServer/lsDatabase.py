"""
Created on Tue Jul  23 2021

@author: Ace Abdulrahman
"""

import sqlite3 as sq
import hashlib

def toHash(pwd):
    ret = hashlib.sha256(pwd.encode()).hexdigest()
    return ret


def createDB():
    try:
        db = sq.connect("local.db")                #Connects to database (db) file
        crsr = db.cursor()                          #cursor used to edit db file     
        crsr.execute("""CREATE TABLE user (         
                            username TEXT,
                            password TEXT)""")      
        pwd= toHash('pfsense')
        crsr.execute('INSERT INTO user VALUES (?,?)',('user', pwd))
        db.commit()
        db.close()                                  #Commit changes and close file
    except sq.OperationalError:
        pass   

def showTokens():                               #Displays rows in table without headers
    with sq.connect("local.db") as db:
        crsr= db.cursor()
        crsr.execute("SELECT rowid, * FROM users")
        x= crsr.fetchall()
    return x

def clearTable():
    with sq.connect("local.db") as db:
        crsr= db.cursor()
        crsr.execute("DELETE FROM user")

def updatePassword(newPwd):
    with sq.connect("local.db") as db:
        crsr= db.cursor()
        pwd= toHash(newPwd)
        crsr.execute("UPDATE user SET password = (?) WHERE rowid=(?)", (pwd, 1))

def isPwd(username, pwd):
    pwd = toHash(pwd)
    with sq.connect('local.db') as db:
        crsr = db.cursor()
        if crsr.execute("SELECT * FROM user WHERE username = (?) AND password = (?)", (username,pwd)).fetchone():
            return True
        
        else:
            return False