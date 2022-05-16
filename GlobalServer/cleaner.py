"""
Created on 6/29/2021

@author: Brooks Robinson
"""
import ipaddress

def order(file):
    f = open(file)
    lst = []
    for aline in f:
        aline = aline.strip()
        lst.append(aline)
    sortedkey = sorted(lst, key=ipaddress.IPv4Address)
    replace = ''
    for ip in sortedkey:
        replace += str(ip) + '\n'
    with open(file, "w") as myfile:
        myfile.write(replace)

if __name__ == '__main__':
    order("IP_address.txt")

