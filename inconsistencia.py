import threading
import random
import time
import tkinter as tk

conteo_personas = 0

root = tk.Tk()
root.title("Conteo de Personas")
label = tk.Label(root, text="Personas en la sala: 0", font=("Arial", 24))
label.pack()

def actualizar_fondo():
    label.config(text=f"Personas en la sala: {conteo_personas}")
    root.after(100, actualizar_fondo)

def simular_evento(puerta):
    global conteo_personas
    evento = random.choice(["entrada", "salida"])
    if evento == "entrada":
        conteo_personas += 1
        print(f"Persona entra por la puerta {puerta}")
    else:
        if conteo_personas > 0:
            conteo_personas -= 1
            print(f"Persona sale por la puerta {puerta}")
        else:
            print(f"No hay personas en la sala para salir por la puerta {puerta}")
    time.sleep(random.uniform(1, 5))

def simular_puerta(puerta):
    while True:
        simular_evento(puerta)

puertas = 5
hilos = []
for i in range(puertas):
    hilo = threading.Thread(target=simular_puerta, args=(i+1,))
    hilos.append(hilo)
    hilo.start()

actualizar_fondo()
root.mainloop()