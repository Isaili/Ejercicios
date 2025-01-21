from threading import Thread, current_thread, active_count,excepthook
from time import sleep
import random
import threading

myvars = threading.local()


class myThread(Thread):
    def __init__(self, tiempo):
        Thread.__init__(self)  
        self.tiempo = tiempo 
    def run(self):
     
     
        print(f"Running {current_thread().name} with delay: {self.tiempo}")
        sleep(self.tiempo)
        print(f"{current_thread().name} finished")


def thread1(tiempo):
    print(f"Running Thread 1: {current_thread().name}")
    sleep(tiempo)
    print(f"Thread 1 finished: {current_thread().name}")

def thread2(valor):
    print(f"Running Thread 2: {current_thread().name}")
    if valor > 3:
        raise Exception("Thread 2 is not allowed to run")
    sleep(valor)
    print(f"Thread 2 finished: {current_thread().name}")


def hook(args):
    print(f"Hook called with args: ", args.exc_info)
#
hilos = []
for i in range(10):
    t1 = myThread(random.uniform(0, 5))
    hilos.append(t1)
    t1.start()


for hx in hilos:
    hx.join()

print(f"Active threads: {active_count()}")


h1 = Thread(target=thread1, args=(5,), name="isai")
h2 = Thread(target=thread2, args=(3,), name="kirito")

h1.start()
h2.start()


sleep(2)
if h1.is_alive():
    print("Thread 1 is alive")


h1.join()
print("Program finished")