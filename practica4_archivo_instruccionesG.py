import turtle
import tkinter as tk
from tkinter import filedialog, messagebox

# --- Configuración Inicial de Turtle y Ventana ---

# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("Dibujante de Instrucciones de Archivo")

# Configuración del Canvas (área de dibujo) de 600x600
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600
canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
# Usar 'top' y 'both' para que el canvas se expanda si la ventana cambia de tamaño
canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Configuración de Turtle dentro del canvas de Tkinter
t = turtle.TurtleScreen(canvas)
t.screensize(CANVAS_WIDTH, CANVAS_HEIGHT) # Establecer el área lógica de la pantalla
pincel = turtle.RawTurtle(t)
pincel.speed(2) # Configurar la velocidad del puntero

# Inicializar parámetros de estado (usados en las funciones de dibujo)
parametros = {
    "cuadrado": {"color": "blue", "grosor": 3, "lado": 100},
    "triangulo": {"color": "green", "grosor": 3, "lado": 100},
    "circulo": {"color": "red", "grosor": 3, "radio": 50},
    "linea": {"color": "purple", "grosor": 3, "distancia": 400}, # 'distancia' se usará como un largo simple para la línea
}
# Establecer color y grosor iniciales del pincel
pincel.color(parametros["cuadrado"]["color"])
pincel.pensize(parametros["cuadrado"]["grosor"])

# --- Funciones de Dibujo (Adaptadas para usar la posición actual del pincel) ---

def dibujar_cuadrado():
    """ Dibuja un cuadrado de lado fijo a partir de la posición actual. """
    p = parametros["cuadrado"]
    pincel.pendown()
    pincel.color(p["color"])
    pincel.pensize(p["grosor"])
    for _ in range(4):
        pincel.forward(p["lado"])
        pincel.left(90)
    pincel.penup()

def dibujar_triangulo():
    """ Dibuja un triángulo equilátero de lado fijo a partir de la posición actual. """
    p = parametros["triangulo"]
    pincel.pendown()
    pincel.color(p["color"])
    pincel.pensize(p["grosor"])
    for _ in range(3):
        pincel.forward(p["lado"])
        pincel.left(120)
    pincel.penup()

def dibujar_circulo():
    """ Dibuja un círculo de radio fijo. """
    p = parametros["circulo"]
    # Mover el pincel a la posición inicial (abajo del centro para el dibujo de circle)
    pos_x, pos_y = pincel.position()
    pincel.goto(pos_x, pos_y - p["radio"])
    
    pincel.pendown()
    pincel.color(p["color"])
    pincel.pensize(p["grosor"])
    pincel.circle(p["radio"])

    # Regresar a la posición inicial después de dibujar el círculo
    pincel.penup()
    pincel.goto(pos_x, pos_y)

def dibujar_linea():
    """ Dibuja una línea horizontal de largo fijo a partir de la posición actual. """
    p = parametros["linea"]
    pincel.pendown()
    pincel.color(p["color"])
    pincel.pensize(p["grosor"])
    pincel.forward(p["distancia"])
    pincel.penup()

def teleport(x, y):
    """ Mueve el pincel a las coordenadas (x, y) sin dibujar (penup). """
    pincel.penup()
    pincel.goto(x, y)

# --- Procesamiento del Archivo de Instrucciones ---

def procesar_instrucciones(nombre_archivo):
    """
    Abre y procesa el archivo de instrucciones línea por línea.
    Ejecuta las acciones válidas y emite warnings para las inválidas.
    """
    try:
        try:
            # Intenta abrir el archivo con la codificación estándar UTF-8
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                lineas = archivo.readlines()
        except UnicodeDecodeError:
            # Si UTF-8 falla, intenta con una codificación más flexible como 'latin-1'
            print("Advertencia: No se pudo decodificar el archivo como UTF-8. Intentando con 'latin-1'.")
            with open(nombre_archivo, 'r', encoding='latin-1') as archivo:
                lineas = archivo.readlines()

        print(f"--- Procesando archivo: {nombre_archivo} ---")
        pincel.penup() # Asegurar que no dibuje al inicio
        pincel.home()  # Poner el pincel en el centro (0, 0)
        pincel.clear() # Limpiar la pantalla de cualquier dibujo anterior

        for num_linea, linea in enumerate(lineas, 1):
            instruccion = linea.strip().lower() 
            
            # Ignorar líneas vacías o comentarios (que empiezan con #)
            if not instruccion or instruccion.startswith('#'):
                continue

            partes = instruccion.split()
            comando = partes[0]

            if comando == "dibujar_cuadrado":
                dibujar_cuadrado()
            
            elif comando == "dibujar_triangulo":
                dibujar_triangulo()
            
            elif comando == "dibujar_circulo":
                dibujar_circulo()
            
            elif comando == "dibujar_linea":
                dibujar_linea()
            
            elif comando == "teleport":
                if len(partes) == 3:
                    try:
                        x = int(partes[1])
                        y = int(partes[2])
                        teleport(x, y)
                    except ValueError:
                        print(f"[WARNING - Línea {num_linea}]: Error en parámetros de 'teleport'. Se esperan números enteros. Ignorando: {linea.strip()}")
                else:
                    print(f"[WARNING - Línea {num_linea}]: Instrucción 'teleport' incompleta. Se esperan 2 coordenadas. Ignorando: {linea.strip()}")
            
            else:
                print(f"[WARNING - Línea {num_linea}]: Instrucción no válida. Ignorando: {linea.strip()}")

    except FileNotFoundError:
        messagebox.showerror("Error de Archivo", f"El archivo '{nombre_archivo}' no se encontró.")
        print(f"ERROR: El archivo '{nombre_archivo}' no se encontró.")
    except Exception as e:
        messagebox.showerror("Error Inesperado", f"Ocurrió un error al leer el archivo: {e}")
        print(f"Ocurrió un error inesperado al leer el archivo: {e}")

# --- Ejecución Principal e Interfaz de Usuario ---

def iniciar_proceso_de_dibujo():
    """
    Abre un diálogo para que el usuario seleccione un archivo de instrucciones
    y luego lo procesa para dibujar en el canvas.
    """
    try:
        nombre_archivo = filedialog.askopenfilename(
            title="Seleccionar archivo de instrucciones",
            filetypes=[("Archivos de Texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        # Si el usuario selecciona un archivo (no cancela el diálogo)
        if nombre_archivo:
            procesar_instrucciones(nombre_archivo)
        else:
            print("Selección de archivo cancelada por el usuario.")
            
    except Exception as e:
        messagebox.showerror("Error", f"Ha ocurrido un error inesperado: {e}")
        print(f"Ha ocurrido un error inesperado durante la ejecución: {e}")

# Crear un Frame para contener el botón y mejorar el layout
frame_controles = tk.Frame(root)
frame_controles.pack(side=tk.BOTTOM, pady=5, padx=10, fill='x')

# Botón para cargar el archivo
boton_cargar = tk.Button(
    frame_controles, 
    text="Cargar y Dibujar desde Archivo", 
    command=iniciar_proceso_de_dibujo
)
boton_cargar.pack()

# Mantener la ventana abierta
root.mainloop()

