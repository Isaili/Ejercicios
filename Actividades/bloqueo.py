import threading
import time

bloqueo = threading.Lock()
def fnc_a():
    print("iniciando la funcion 4")
    with bloqueo:
        print("seccion critia a")
        time.sleep(2)
        fnc_b()
        print("seccion critica a-fn")

def fnc_b():
    print("iniciando funcion b")
    with bloqueo:
        print("iniciando seccion critica b")
        time.sleep(3)
        print("inicioando seccion critica d")

def main():
    h1 = threading.Thread(target=fnc_a,name="hilo1")
    h2 = threading.Thread(target=fnc_a,name="hilo2")
    h1.start()
    h2.start()
    
    h1.join()
    h2.join()
    
if __name__=="__main__":
    main()