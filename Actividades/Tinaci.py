import threading
import time
from tkinter import Tk, Canvas, Label, Frame, Button, ttk, HORIZONTAL

# Variables globales
nivel_agua = 100  # Nivel inicial del tinaco (en %)
lock = threading.Lock()

# Semáforos
semaforo_bomba = threading.Semaphore(1)
semaforo_jardin = threading.Semaphore(1)
semaforo_lavadero = threading.Semaphore(1)

# Estados de las tomas
estado_jardin = False
estado_lavadero = False
bomba_activa = False

def control_bomba():
    global nivel_agua, bomba_activa
    while True:
        with lock:
            if nivel_agua < 100 and bomba_activa:
                semaforo_bomba.acquire()
                nivel_agua = min(100, nivel_agua + 10)  # Evitar que supere 100%
                time.sleep(1)
                semaforo_bomba.release()
        time.sleep(2)

def control_tomas(toma, porcentaje_corte):
    global nivel_agua
    while True:
        with lock:
            if (toma == "jardín" and estado_jardin and nivel_agua > porcentaje_corte) or \
               (toma == "lavadero" and estado_lavadero and nivel_agua > porcentaje_corte):
                nivel_agua = max(0, nivel_agua - 5)  # Evitar que baje de 0%
                time.sleep(2)
        time.sleep(2)

class InterfazTinaco:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Control de Tinaco")
        self.root.geometry("600x500")
        self.root.configure(bg='#f0f0f0')
        
        self.setup_ui()
        self.iniciar_actualizacion()

    def setup_ui(self):
        # Frame principal
        main_frame = Frame(self.root, bg='#f0f0f0')
        main_frame.pack(padx=20, pady=20, expand=True, fill='both')

        # Frame izquierdo para el tanque
        left_frame = Frame(main_frame, bg='#f0f0f0')
        left_frame.pack(side='left', padx=20, fill='both', expand=True)

        # Canvas para el tinaco
        self.canvas = Canvas(left_frame, width=200, height=300, bg='white')
        self.canvas.pack(pady=10)

        # Etiqueta de nivel
        self.label_nivel = Label(left_frame, 
                               text="Nivel de agua: 100%",
                               font=("Arial", 12, "bold"),
                               bg='#f0f0f0')
        self.label_nivel.pack(pady=10)

        # Barra de progreso
        self.progress = ttk.Progressbar(left_frame, 
                                      orient=HORIZONTAL,
                                      length=200, 
                                      mode='determinate')
        self.progress.pack(pady=10)

        # Frame derecho para controles
        right_frame = Frame(main_frame, bg='#f0f0f0')
        right_frame.pack(side='right', padx=20, fill='both')

        # Frame para los controles
        controls_frame = Frame(right_frame, bg='#f0f0f0')
        controls_frame.pack(pady=20)

        # Título de controles
        Label(controls_frame, 
              text="Panel de Control",
              font=("Arial", 14, "bold"),
              bg='#f0f0f0').pack(pady=10)

        # Botón de la bomba
        self.btn_bomba = Button(controls_frame,
                               text="Activar Bomba",
                               command=self.toggle_bomba,
                               width=15,
                               height=2)
        self.btn_bomba.pack(pady=10)

        # Botón del jardín
        self.btn_jardin = Button(controls_frame,
                                text="Abrir Jardín",
                                command=self.toggle_jardin,
                                width=15,
                                height=2)
        self.btn_jardin.pack(pady=10)

        # Botón del lavadero
        self.btn_lavadero = Button(controls_frame,
                                  text="Abrir Lavadero",
                                  command=self.toggle_lavadero,
                                  width=15,
                                  height=2)
        self.btn_lavadero.pack(pady=10)

        # Frame para el estado
        status_frame = Frame(right_frame, bg='#f0f0f0')
        status_frame.pack(pady=20, fill='x')

        # Etiquetas de estado
        self.label_estado_bomba = Label(status_frame,
                                      text="Bomba: Inactiva",
                                      bg='#f0f0f0')
        self.label_estado_bomba.pack(pady=5)

        self.label_estado_jardin = Label(status_frame,
                                       text="Jardín: Cerrado",
                                       bg='#f0f0f0')
        self.label_estado_jardin.pack(pady=5)

        self.label_estado_lavadero = Label(status_frame,
                                         text="Lavadero: Cerrado",
                                         bg='#f0f0f0')
        self.label_estado_lavadero.pack(pady=5)

    def toggle_bomba(self):
        global bomba_activa
        bomba_activa = not bomba_activa
        self.btn_bomba.config(text="Desactivar Bomba" if bomba_activa else "Activar Bomba")
        self.label_estado_bomba.config(text=f"Bomba: {'Activa' if bomba_activa else 'Inactiva'}")

    def toggle_jardin(self):
        global estado_jardin
        estado_jardin = not estado_jardin
        self.btn_jardin.config(text="Cerrar Jardín" if estado_jardin else "Abrir Jardín")
        self.label_estado_jardin.config(text=f"Jardín: {'Abierto' if estado_jardin else 'Cerrado'}")

    def toggle_lavadero(self):
        global estado_lavadero
        estado_lavadero = not estado_lavadero
        self.btn_lavadero.config(text="Cerrar Lavadero" if estado_lavadero else "Abrir Lavadero")
        self.label_estado_lavadero.config(text=f"Lavadero: {'Abierto' if estado_lavadero else 'Cerrado'}")

    def dibujar_tinaco(self):
        self.canvas.delete("all")
        
        # Dibujar el tanque
        self.canvas.create_rectangle(50, 50, 150, 300, outline="black", width=2)
        
        # Calcular altura del agua
        altura_agua = 250 * (nivel_agua / 100)
        y_agua = 300 - altura_agua
        
        # Dibujar el agua
        if nivel_agua > 0:
            self.canvas.create_rectangle(50, y_agua, 150, 300,
                                       fill="#3498db")  # Color azul para el agua
            
        # Añadir marcas de nivel
        for i in range(0, 101, 20):
            y = 300 - (250 * (i / 100))
            self.canvas.create_line(45, y, 50, y)
            self.canvas.create_text(35, y, text=f"{i}%")

    def actualizar_interfaz(self):
        with lock:
            self.label_nivel.config(text=f"Nivel de agua: {nivel_agua}%")
            self.progress['value'] = nivel_agua
            self.dibujar_tinaco()
        self.root.after(100, self.actualizar_interfaz)

    def iniciar_actualizacion(self):
        self.actualizar_interfaz()

def main():
    root = Tk()
    app = InterfazTinaco(root)
    
    # Crear hilos
    hilo_bomba = threading.Thread(target=control_bomba)
    hilo_jardin = threading.Thread(target=control_tomas, args=("jardín", 50))
    hilo_lavadero = threading.Thread(target=control_tomas, args=("lavadero", 30))
    
    # Configurar hilos como daemon
    hilo_bomba.daemon = True
    hilo_jardin.daemon = True
    hilo_lavadero.daemon = True
    
    # Iniciar hilos
    hilo_bomba.start()
    hilo_jardin.start()
    hilo_lavadero.start()
    
    root.mainloop()

if __name__ == "__main__":
    main()