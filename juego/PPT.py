import tkinter as tk
import random

def jugar(jugador1):
    opciones = ["piedra", "papel", "tijera"]
    eleccion = random.choice(opciones)
    
   
    if jugador1 == eleccion:
        resultado.set(f"¡Empataron! Ambos eligieron {jugador1}.")
    elif (jugador1 == "piedra" and eleccion == "tijera") or \
         (jugador1 == "tijera" and eleccion == "papel") or \
         (jugador1 == "papel" and eleccion == "piedra"):
        resultado.set(f"¡Ganaste! {jugador1} vence a {eleccion}.")
    else:
        resultado.set(f"¡Perdiste! {eleccion} vence a {jugador1}.")

# Crear la ventana
ventana = tk.Tk()
ventana.title("Juego de Piedra, Papel o Tijera")

resultado = tk.StringVar()
resultado.set("Selecciona una opción para jugar.")

etiqueta_resultado = tk.Label(ventana, textvariable=resultado, font=("Arial", 12), wraplength=300, justify="center")
etiqueta_resultado.pack(pady=10)

boton_piedra = tk.Button(ventana, text="🪨 Piedra", font=("Arial", 14), command=lambda: jugar("piedra"))
boton_piedra.pack(pady=5)

boton_papel = tk.Button(ventana, text="📄 Papel", font=("Arial", 14), command=lambda: jugar("papel"))
boton_papel.pack(pady=5)

boton_tijera = tk.Button(ventana, text="✂️ Tijera", font=("Arial", 14), command=lambda: jugar("tijera"))
boton_tijera.pack(pady=5)

boton_salir = tk.Button(ventana, text="Salir", font=("Arial", 12), command=ventana.quit, bg="red", fg="white")
boton_salir.pack(pady=10)

ventana.mainloop()
