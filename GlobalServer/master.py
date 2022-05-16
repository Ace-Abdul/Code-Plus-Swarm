import os, time

os.system('chmod +x install.sh makeConfigFile.py path.py pull.sh')
os.system('./install.sh')
#time.sleep(10)
count = 0

while True and count<10:
    os.system("./pull.sh")
    count+=1
    time.sleep(10)
    
