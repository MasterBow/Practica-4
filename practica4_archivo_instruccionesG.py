# ===============================================================
# Proyecto: P4 Dibujante de Instrucciones desde Archivo de Texto
# Autor: Raúl Alexi Rodriguez Fong 21760180

# ===============================================================

# Importamos las librerías necesarias
import turtle       # Para dibujar figuras en pantalla
import tkinter as tk   # Para crear la ventana y los widgets
from tkinter import filedialog, messagebox  # Para diálogos y alertas

# ===============================================================
# 1. CONFIGURACIÓN DE LA VENTANA PRINCIPAL
# ===============================================================

# Crear la ventana principal de Tkinter
root = tk.Tk()  # Tk() crea una ventana vacía
root.title("Dibujante de Instrucciones de Archivo")  # Título de la ventana

# Definir dimensiones del área de dibujo
CANVAS_WIDTH = 600   # Ancho del canvas
CANVAS_HEIGHT = 600  # Alto del canvas

# Crear el canvas (área donde Turtle dibujará)
canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
# Empaquetar el canvas en la ventana. fill=BOTH permite que se expanda al cambiar la ventana
canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# ===============================================================
# 2. CONFIGURACIÓN DE TURTLE DENTRO DEL CANVAS
# ===============================================================

# Crear pantalla de Turtle ligada al canvas de Tkinter
t = turtle.TurtleScreen(canvas)
t.screensize(CANVAS_WIDTH, CANVAS_HEIGHT)  # Área lógica de dibujo (coordenadas)

# Crear un objeto Turtle (el "pincel") para dibujar
pincel = turtle.RawTurtle(t)
pincel.speed(2)  # Velocidad de dibujo: 1 lenta, 10 rápida, 0 instantáneo

# ===============================================================
# 3. PARÁMETROS DE FIGURAS
# ===============================================================

# Diccionario con parámetros para cada tipo de figura
# Facilita cambiar colores, tamaños o grosor sin modificar cada función
parametros = {
    "cuadrado": {"color": "blue", "grosor": 3, "lado": 100},
    "triangulo": {"color": "green", "grosor": 3, "lado": 100},
    "circulo": {"color": "red", "grosor": 3, "radio": 50},
    "linea": {"color": "purple", "grosor": 3, "distancia": 400},
}

# Establecemos color y grosor inicial del pincel
pincel.color(parametros["cuadrado"]["color"])
pincel.pensize(parametros["cuadrado"]["grosor"])

# ===============================================================
# 4. FUNCIONES DE DIBUJO
# ===============================================================

def dibujar_cuadrado():
    """
    Dibuja un cuadrado de lado fijo a partir de la posición actual del pincel.
    Explicación Turtle:
    - pendown(): baja el lápiz para dibujar
    - forward(lado): avanza "lado" píxeles
    - left(90): gira 90° a la izquierda
    - penup(): levanta el lápiz para moverse sin dibujar
    """
    p = parametros["cuadrado"]  # Extraemos parámetros
    pincel.pendown()
    pincel.color(p["color"])
    pincel.pensize(p["grosor"])
    for _ in range(4):
        pincel.forward(p["lado"])
        pincel.left(90)
    pincel.penup()

def dibujar_triangulo():
    """
    Dibuja un triángulo equilátero desde la posición actual.
    Explicación Turtle:
    - left(120): ángulo interno de un triángulo equilátero
    """
    p = parametros["triangulo"]
    pincel.pendown()
    pincel.color(p["color"])
    pincel.pensize(p["grosor"])
    for _ in range(3):
        pincel.forward(p["lado"])
        pincel.left(120)
    pincel.penup()

def dibujar_circulo():
    """
    Dibuja un círculo centrado en la posición actual.
    Explicación:
    - circle(radio) dibuja un círculo con el radio indicado
    - Ajustamos posición para que el círculo quede centrado
    """
    p = parametros["circulo"]
    pos_x, pos_y = pincel.position()  # Guardamos posición actual
    pincel.goto(pos_x, pos_y - p["radio"])  # Ajustamos para que el círculo quede centrado
    pincel.pendown()
    pincel.color(p["color"])
    pincel.pensize(p["grosor"])
    pincel.circle(p["radio"])
    pincel.penup()
    pincel.goto(pos_x, pos_y)  # Volvemos a la posición original

def dibujar_linea():
    """
    Dibuja una línea horizontal de longitud fija.
    """
    p = parametros["linea"]
    pincel.pendown()
    pincel.color(p["color"])
    pincel.pensize(p["grosor"])
    pincel.forward(p["distancia"])
    pincel.penup()

def teleport(x, y):
    """
    Mueve el pincel a coordenadas (x, y) sin dibujar.
    Explicación:
    - penup(): levantamos el lápiz para no dibujar al movernos
    - goto(x, y): mueve el pincel a la posición indicada
    """
    pincel.penup()
    pincel.goto(x, y)

# ===============================================================
# 5. PROCESAMIENTO DE ARCHIVO DE INSTRUCCIONES
# ===============================================================

def procesar_instrucciones(nombre_archivo):
    """
    Lee un archivo de texto línea por línea y ejecuta comandos válidos.
    Maneja errores de codificación, archivo no encontrado y parámetros incorrectos.
    """
    try:
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                lineas = archivo.readlines()
        except UnicodeDecodeError:
            # Si UTF-8 falla, usamos Latin-1
            print("Advertencia: Fallo al decodificar UTF-8. Intentando Latin-1.")
            with open(nombre_archivo, 'r', encoding='latin-1') as archivo:
                lineas = archivo.readlines()

        print(f"--- Procesando archivo: {nombre_archivo} ---")
        pincel.penup()
        pincel.home()  # Mover al centro
        pincel.clear()  # Limpiar canvas

        for num_linea, linea in enumerate(lineas, 1):
            instruccion = linea.strip().lower()  # Normalizamos
            if not instruccion or instruccion.startswith('#'):
                continue  # Ignoramos comentarios o líneas vacías

            partes = instruccion.split()
            comando = partes[0]

            # Ejecutar comandos válidos
            if comando == "dibujar_cuadrado":
                dibujar_cuadrado()
            elif comando == "dibujar_triangulo":
                dibujar_triangulo()
            elif comando == "dibujar_circulo":
                dibujar_circulo()
            elif comando == "dibujar_linea":
                dibujar_linea()
            elif comando == "teleport":
                # Validamos que haya 2 parámetros numéricos
                if len(partes) == 3:
                    try:
                        x = int(partes[1])
                        y = int(partes[2])
                        teleport(x, y)
                    except ValueError:
                        print(f"[WARN - Línea {num_linea}] 'teleport' requiere números enteros.")
                else:
                    print(f"[WARN - Línea {num_linea}] 'teleport' necesita 2 coordenadas.")
            else:
                print(f"[WARN - Línea {num_linea}] Comando desconocido: {linea.strip()}")

    except FileNotFoundError:
        messagebox.showerror("Error de Archivo", f"Archivo '{nombre_archivo}' no encontrado.")
        print(f"ERROR: Archivo '{nombre_archivo}' no encontrado.")
    except Exception as e:
        messagebox.showerror("Error Inesperado", f"Ocurrió un error al leer el archivo: {e}")
        print(f"ERROR inesperado: {e}")

# ===============================================================
# 6. INTERFAZ DE USUARIO
# ===============================================================

def iniciar_proceso_de_dibujo():
    """
    Abre un diálogo para seleccionar archivo y procesa las instrucciones.
    """
    try:
        nombre_archivo = filedialog.askopenfilename(
            title="Seleccionar archivo de instrucciones",
            filetypes=[("Archivos de Texto", "*.txt"), ("Todos los archivos", "*.*")]
        )

        if nombre_archivo:
            procesar_instrucciones(nombre_archivo)
        else:
            print("Usuario canceló la selección de archivo.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")
        print(f"ERROR inesperado durante la ejecución: {e}")

# Frame para el botón
frame_controles = tk.Frame(root)
frame_controles.pack(side=tk.BOTTOM, pady=5, padx=10, fill='x')

# Botón para iniciar el proceso
boton_cargar = tk.Button(
    frame_controles,
    text="Cargar y Dibujar desde Archivo",
    command=iniciar_proceso_de_dibujo
)
boton_cargar.pack()

# ===============================================================
# 7. INICIAR LA APLICACIÓN
# ===============================================================

root.mainloop()  # Mantiene la ventana abierta y responde a eventos
