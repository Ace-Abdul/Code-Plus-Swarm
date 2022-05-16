"""
Created on 6/29/2021

@author: Brooks Robinson
"""

def append(original, new):
    f1 = open(original)
    lst1 = []
    for aline in f1:
        aline = aline.strip()
        lst1.append(aline)

    f2 = open(new)
    lst2 = []
    for aline in f2:
        aline = aline.strip()
        lst2.append(aline)

    newlst = []
    for ip in lst2:
        if ip not in lst1:
            newlst.append(ip)

    new = ''
    for i in range(len(newlst)):
        ip = newlst[i]
        if i == 0:
            new += str(ip)
        else:
            new += '\n' + str(ip)

    with open(original, "a") as myfile:
        myfile.write(new)

if __name__ == '__main__':
    append("IP_address.txt", "temp.txt")
