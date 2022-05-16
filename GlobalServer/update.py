"""
Created on 6/30/2021

Create dictionary with "IP address" as key, "last seen time" as value.
For each key, check if "last seen time" > 7. If yes, add key to list "rm".
For each IP address in "rm", delete from dictionary.
Overwrite IP_address.txt to only include IP addresses whose "last seen time" < 7.
"""
from datetime import datetime, timedelta
store_dict = {}

def dict_maker(ipaddresstimefile, storefile):
    f1 = open(storefile)
    for aline in f1:
        aline = aline.strip()
        temp = aline.split(',')
        temp[1] = temp[1].split('T')
        ip = temp[0]
        time = temp[1][0]
        store_dict[ip] = time
    #print(store_dict)


    f2 = open(ipaddresstimefile)
    for aline in f2:
        aline = aline.strip()
        temp = aline.split(',')
        temp[1] = temp[1].split('T')
        ip = temp[0]
        time = temp[1][0]
        store_dict[ip] = time
    #print(store_dict)
    checker(store_dict)

def checker(dict):
    ini_time_for_now = str(str(datetime.today()).split()[0])
    rm = []
    ini_time_for_now = ini_time_for_now.split('-')
    now = datetime(int(ini_time_for_now[0]), int(ini_time_for_now[1]), int(ini_time_for_now[2]))
    #print("This is now", now)
    for ip, time in dict.items():
        time = time.split('-')
        then = datetime(int(time[0]), int(time[1]), int(time[2]))
        #print("This is then:", then)
        if (now - then).days < 7:
            #print("good:", ip)
            continue
        else:
            #print("bad:", ip)
            rm.append(ip)
    remover(rm, dict, "IP_address.txt", "store.txt")

def remover(rm, dict, file_to_overwrite, file_to_store):
    #print("This is original dict:", dict)
    for ip in rm:
        del dict[ip]
    #print("This is new dict:", dict)
    keys = list(dict.keys())
    new = ''
    for i in range(len(keys)):
        ip = keys[i]
        if i == (len(dict.keys()) -1):
            new += str(ip)
        else:
            new += str(ip) + '\n'

    ini_time_for_now = str(str(datetime.today()).split()[0])
    ini_time_for_now = ini_time_for_now.split('-')
    now = datetime(int(ini_time_for_now[0]), int(ini_time_for_now[1]), int(ini_time_for_now[2]))

    store = ''
    for i in range(len(keys)):
        ip = keys[i]
        time = dict[ip]
        time = time.split('-')
        then = datetime(int(time[0]), int(time[1]), int(time[2]))
        if (now - then).days > 7:
            continue
        if i == (len(dict.keys()) -1):
            store += str(ip) + "," + str(dict[ip])
        else:
            store += str(ip) + "," + str(dict[ip]) + '\n'

    with open(file_to_overwrite, "w") as myfile:
        myfile.write(new)
    with open(file_to_store, "w") as myfile:
        myfile.write(store)

if __name__ == '__main__':
    dict_maker('IP_address_time.txt', 'store.txt')