"""
    Holds the functions for hashing passwords, checking if the passwords match, and storing them into the file.
    User and pass input
    
"""
import hashlib


## Hashes password and checks it with the one on file
def hashAndCheck(user, ps):
    passfile = open('storeUserPassword.txt', 'r')
    userPass = passfile.readlines()
    password = hashlib.sha256(ps.encode()).hexdigest()

    ## Code goes here that reads file and matches user 
    if user == userPass[0].strip() and password == userPass[1].strip():
         return True
    else:
         return False


## Hashes password and replaces the old user and password on file
def hashAndReplace(user, ps):
    passfile = open('storeUserPassword.txt', 'w')
    password = hashlib.sha256(ps.encode()).hexdigest()

    lst = [user + '\n', password]
    passfile.writelines(lst)



