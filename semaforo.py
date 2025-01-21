import threading
import time

x=0
sem = threading.Semaphore(0)
def region_c(num):
    global x
    time.sleep(2)
    x = x + num
    print("el hilo"+str(id+"el valorde x es "+str(x)))

def hilo(num):
    sem.acquire()
    region_c(num)
    sem.release()
    
def main():
    hilos = []
    for i in range(10): 
     h1 = threading.Thread(target=hilo, args=(i,1))
     hilos.append(h1)

     for hx in hilos:
         hx.start()
  
     for hx in hilos:
         hx.join()
if __name__ == '__main__':
    main()