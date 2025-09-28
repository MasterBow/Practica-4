# Practica-4

## Documentación del Programa "Dibujante con Turtle"
Descripción General 
Este programa es una aplicación de escritorio que permite dibujar figuras geométricas en una ventana a partir de un conjunto de instrucciones leídas desde un archivo de texto. Utiliza la biblioteca tkinter para crear la interfaz gráfica (la ventana y el botón) y la biblioteca turtle para realizar los dibujos sobre un lienzo (canvas).

El objetivo principal es interpretar comandos simples de un archivo de texto, como "dibujar un cuadrado" o "moverse a una coordenada", y traducirlos en acciones gráficas.

##Componentes Principales 
El código se divide en varias partes lógicas:

## 1. Configuración de la Interfaz Gráfica (Tkinter)
root = tk.Tk(): Crea la ventana principal de la aplicación.

canvas = tk.Canvas(...): Crea un lienzo o área de dibujo dentro de la ventana principal. Este es el espacio donde turtle dibujará.

frame_controles y boton_cargar: Crean un contenedor (Frame) y un botón ("Cargar y Dibujar desde Archivo"). Este botón es el que inicia la acción de leer un archivo y dibujar.

## 2. Integración de Turtle
t = turtle.TurtleScreen(canvas): Vincula el sistema de gráficos de turtle directamente al canvas de tkinter.

pincel = turtle.RawTurtle(t): Crea el objeto "tortuga" o "pincel" que se moverá y dibujará sobre el lienzo. Se usa RawTurtle porque es la clase adecuada cuando se integra turtle dentro de tkinter.

## 3. Funciones de Dibujo
El programa define una función para cada figura que puede dibujar y una para moverse:

dibujar_cuadrado(): Dibuja un cuadrado.

dibujar_triangulo(): Dibuja un triángulo equilátero.

dibujar_circulo(): Dibuja un círculo.

dibujar_linea(): Dibuja una línea recta.

teleport(x, y): Mueve el pincel a las coordenadas (x, y) sin dejar rastro.

Todas las funciones de dibujo utilizan los parámetros (color, grosor, tamaño) definidos en el diccionario parametros al inicio del código.

## 4. Procesamiento del Archivo de Instrucciones
Esta es la lógica central del programa, contenida en la función procesar_instrucciones(nombre_archivo).

Apertura Segura del Archivo: Intenta abrir el archivo con codificación utf-8. Si falla (como en el error que tuviste), lo reintenta con latin-1, lo que lo hace más robusto.

Limpieza del Lienzo: Antes de empezar a dibujar, limpia cualquier dibujo previo (pincel.clear()) y coloca el pincel en el centro (pincel.home()).

Lectura Línea por Línea: Recorre el archivo, ignorando líneas vacías y comentarios (líneas que empiezan con #).

Interpretación de Comandos: Para cada línea válida, divide el texto en un comando (la primera palabra, ej: teleport) y sus argumentos (las palabras siguientes, ej: -100 50).

Ejecución: Usa una serie de if/elif para determinar qué función de dibujo llamar según el comando leído. Realiza validaciones, como verificar que teleport reciba dos números enteros.

Manejo de Errores: Si no encuentra el archivo o si ocurre otro problema durante la lectura, muestra una ventana emergente (messagebox) informando al usuario.

## 5. Flujo de Ejecución Principal
La función iniciar_proceso_de_dibujo() se encarga de conectar la interfaz de usuario con la lógica de procesamiento.

Cuando el usuario hace clic en el botón, esta función abre un diálogo de selección de archivo (filedialog.askopenfilename).

Si el usuario selecciona un archivo, la ruta de ese archivo se pasa a la función procesar_instrucciones para que comience el dibujo.

root.mainloop() es la llamada final que mantiene la ventana abierta y a la espera de acciones del usuario (como hacer clic en el botón).

## ¿Cómo se Usa? 
Ejecuta el script de Python. Aparecerá una ventana con un área de dibujo en blanco y un botón en la parte inferior.

Haz clic en el botón "Cargar y Dibujar desde Archivo".

Se abrirá un explorador de archivos. Selecciona un archivo .txt que contenga las instrucciones de dibujo.

El programa leerá el archivo y dibujará las figuras correspondientes en el lienzo.

El archivo de instrucciones debe contener comandos válidos, uno por línea. Ejemplo:

# TXT
teleport -200 150
dibujar_cuadrado

teleport 100 150
dibujar_triangulo

teleport 0 -50
dibujar_circulo

teleport -200 -200
dibujar_linea

dibujar_pentagono # Esto generará un warning

teleport 150 0
dibujar_cuadrado


teleport 0 0
dibujar_circulo
