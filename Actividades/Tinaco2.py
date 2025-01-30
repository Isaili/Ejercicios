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
                if nivel_agua >= 100:  # Si está lleno, desactivar bomba
                    bomba_activa = False
                else:
                    semaforo_bomba.acquire()
                    nivel_agua = min(100, nivel_agua + 10)
                    time.sleep(1)
                    semaforo_bomba.release()
        time.sleep(2)

def control_tomas(toma, porcentaje_corte):
    global nivel_agua, estado_jardin, estado_lavadero
    while True:
        with lock:
            # Cerrar todas las tomas si el nivel es muy bajo (5%)
            if nivel_agua <= 5:
                estado_jardin = False
                estado_lavadero = False
            
            # Control del jardín
            elif toma == "jardín":
                if nivel_agua <= 50:  # Cerrar jardín si nivel <= 50%
                    estado_jardin = False
                elif estado_jardin:
                    nivel_agua = max(0, nivel_agua - 5)
            
            # Control del lavadero
            elif toma == "lavadero":
                if nivel_agua <= 30:  # Cerrar lavadero si nivel <= 30%
                    estado_lavadero = False
                elif estado_lavadero:
                    nivel_agua = max(0, nivel_agua - 5)
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
                                      bg='#f0f0f0',
                                      font=("Arial", 10))
        self.label_estado_bomba.pack(pady=5)

        self.label_estado_jardin = Label(status_frame,
                                       text="Jardín: Cerrado",
                                       bg='#f0f0f0',
                                       font=("Arial", 10))
        self.label_estado_jardin.pack(pady=5)

        self.label_estado_lavadero = Label(status_frame,
                                         text="Lavadero: Cerrado",
                                         bg='#f0f0f0',
                                         font=("Arial", 10))
        self.label_estado_lavadero.pack(pady=5)

        # Frame para advertencias
        warning_frame = Frame(right_frame, bg='#f0f0f0')
        warning_frame.pack(pady=10, fill='x')

        # Etiqueta de advertencias
        self.label_advertencia = Label(warning_frame,
                                     text="",
                                     bg='#f0f0f0',
                                     fg='red',
                                     wraplength=200,
                                     font=("Arial", 10, "bold"))
        self.label_advertencia.pack(pady=5)

    def toggle_bomba(self):
        global bomba_activa
        if nivel_agua >= 100:
            self.label_advertencia.config(text="No se puede activar la bomba: Tinaco lleno")
            return
        bomba_activa = not bomba_activa
        self.btn_bomba.config(text="Desactivar Bomba" if bomba_activa else "Activar Bomba")
        self.label_estado_bomba.config(text=f"Bomba: {'Activa' if bomba_activa else 'Inactiva'}")
        self.label_advertencia.config(text="")

    def toggle_jardin(self):
        global estado_jardin
        if nivel_agua <= 50:
            self.label_advertencia.config(text="No se puede abrir el jardín: Nivel de agua muy bajo (≤ 50%)")
            return
        estado_jardin = not estado_jardin
        self.btn_jardin.config(text="Cerrar Jardín" if estado_jardin else "Abrir Jardín")
        self.label_estado_jardin.config(text=f"Jardín: {'Abierto' if estado_jardin else 'Cerrado'}")
        self.label_advertencia.config(text="")

    def toggle_lavadero(self):
        global estado_lavadero
        if nivel_agua <= 30:
            self.label_advertencia.config(text="No se puede abrir el lavadero: Nivel de agua muy bajo (≤ 30%)")
            return
        estado_lavadero = not estado_lavadero
        self.btn_lavadero.config(text="Cerrar Lavadero" if estado_lavadero else "Abrir Lavadero")
        self.label_estado_lavadero.config(text=f"Lavadero: {'Abierto' if estado_lavadero else 'Cerrado'}")
        self.label_advertencia.config(text="")

    def dibujar_tinaco(self):
        self.canvas.delete("all")
        
        # Dibujar el tanque
        self.canvas.create_rectangle(50, 50, 150, 300, outline="black", width=2)
        
        # Calcular altura del agua
        altura_agua = 250 * (nivel_agua / 100)
        y_agua = 300 - altura_agua
        
        # Dibujar el agua
        if nivel_agua > 0:
            color_agua = "#3498db"  # Azul normal
            if nivel_agua <= 30:
                color_agua = "#e74c3c"  # Rojo para nivel crítico
            elif nivel_agua <= 50:
                color_agua = "#f1c40f"  # Amarillo para nivel bajo
            self.canvas.create_rectangle(50, y_agua, 150, 300, fill=color_agua)
            
        # Añadir marcas de nivel
        for i in range(0, 101, 20):
            y = 300 - (250 * (i / 100))
            self.canvas.create_line(45, y, 50, y)
            self.canvas.create_text(35, y, text=f"{i}%")
        
        # Añadir marcas especiales
        self.canvas.create_line(40, 300 - (250 * 0.5), 50, 300 - (250 * 0.5), fill="red", width=2)
        self.canvas.create_text(30, 300 - (250 * 0.5), text="50%", fill="red")
        
        self.canvas.create_line(40, 300 - (250 * 0.3), 50, 300 - (250 * 0.3), fill="red", width=2)
        self.canvas.create_text(30, 300 - (250 * 0.3), text="30%", fill="red")

    def actualizar_interfaz(self):
        with lock:
            # Actualizar estado de los botones según nivel de agua
            self.btn_bomba.config(state='disabled' if nivel_agua >= 100 else 'normal')
            self.btn_jardin.config(state='disabled' if nivel_agua <= 50 else 'normal')
            self.btn_lavadero.config(state='disabled' if nivel_agua <= 30 else 'normal')
            
            # Si el nivel es muy bajo, cerrar todo
            if nivel_agua <= 5:
                global estado_jardin, estado_lavadero, bomba_activa
                estado_jardin = False
                estado_lavadero = False
                self.btn_jardin.config(text="Abrir Jardín")
                self.btn_lavadero.config(text="Abrir Lavadero")
                self.label_estado_jardin.config(text="Jardín: Cerrado")
                self.label_estado_lavadero.config(text="Lavadero: Cerrado")
                self.label_advertencia.config(text="¡NIVEL CRÍTICO! Todas las tomas han sido cerradas")
            
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