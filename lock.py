import threading
from time import sleep

control = threading.Lock()

def getachivo1():
    control.acquire()
    print("archivo1(): archivo1")
    f = open("archivo1.txt","w+")
    data= f.readline()
    print(data)
    sleep(4)
    print("getarchivo1(): archivo 1 finalizado")
    
def getachivo2():
    control.acquire()
    print("getarchivo2(): archivo 2")
    f = open("archivo1.txt","w+")
    data= f.readline()
    print(data)
    sleep(4)
    print("getarchivo2(): archivo 2 finalizado")  
    control.release()
    
t1 = threading.Thread(target=getachivo1)
t2 = threading.Thread(target=getachivo2)
    
    
t2.start()
t1.start()
# t1.join()
# t2.join()
