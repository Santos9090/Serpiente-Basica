from tkinter import *
from random import randint
from pynput import keyboard
import time
pantalla = Tk()
pantalla.title("Snake")
ancho_ventana = 620
alto_ventana = 650
ancho_pantalla = pantalla.winfo_screenwidth()
alto_pantalla = pantalla.winfo_screenheight()
x = (ancho_pantalla - ancho_ventana) // 2
y = (alto_pantalla - alto_ventana) // 2
pantalla.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
tamano = 1
DirX = 0
DirY = 0
antiguo = [[None, None]]
manzana = [None, None]
direccionReal = ""


def on_closing():
    # Agregar aquí cualquier limpieza necesaria antes de cerrar la ventana
    pantalla.destroy()  # Cierra la ventana


# Asocia la función on_closing al cierre de ventana
pantalla.protocol("WM_DELETE_WINDOW", on_closing)


def on_key_press(key):
    global DirX, DirY, direccionReal
    try:
        if key.char == 'w' and direccionReal != "sur":
            DirX = 0
            DirY = -1
            direccionReal = "norte"
        elif key.char == 's' and direccionReal != "norte":
            DirX = 0
            DirY = 1
            direccionReal = "sur"
        elif key.char == 'a' and direccionReal != "este":
            DirX = -1
            DirY = 0
            direccionReal = "oeste"
        elif key.char == 'd' and direccionReal != "oeste":
            DirX = 1
            DirY = 0
            direccionReal = "este"
    except AttributeError:
        pass

def cambiarColor(x, y):
    global DirX, DirY, tamano, antiguo
    frames[x][y].configure(bg="lightgreen")
    frames[x][y].update()
    borrar = len(antiguo)-tamano
    if (borrar >= 1):
        for i in range(borrar):
            frames[antiguo[i][0]][antiguo[i][1]].configure(bg="WHITE")
            frames[antiguo[i][0]][antiguo[i][1]].update()
            antiguo.pop(i)
    if not ([x, y] in antiguo):
        antiguo.append([x, y])


def end():
    print("FIN")


def ranManzana():
    X = randint(0, 29)
    Y = randint(0, 29)
    if (not ([X, Y] in antiguo)):
        frames[X][Y].configure(bg="red")
        frames[X][Y].update()
    else:
        ranManzana()

    global manzana
    manzana = [X, Y]


def EmpezarMovimientos(x, y):
    global DirX, DirY, manzana, tamano
    tamano = 1
    vivo = True
    vueltas = 0
    while vivo:
        x += DirX
        y += DirY
        if x < 0:
            vivo = False
            end()
            break
        if y < 0:
            vivo = False
            end()
            break
        if x > 29:
            vivo = False
            end()
            break
        if y > 29:
            vivo = False
            end()
            break
        if ([x, y] in antiguo) and tamano > 1:
            end()
            vivo = False
        cambiarColor(x, y)
        vueltas += 1
        if (x == manzana[0] and y == manzana[1]):
            ranManzana()
            tamano += 1
        pantalla.update()
        time.sleep(0.1)


def reinicio():
    global frames, DirX, DirY
    for i in range(len(frames)):
        for n in range(len(frames[i])):
            frames[i][n].configure(bg="WHITE")
            frames[i][n].update()
    DirX = 0
    DirY = 0


def inicio():
    global antiguo
    antiguo = []
    reinicio()
    inicioX = randint(1, 28)
    inicioY = randint(1, 28)
    frames[inicioX][inicioY].configure(bg="lightgreen")
    frames[inicioX][inicioY].update()
    antiguo = [[inicioX, inicioY]]
    ranManzana()
    try:
        EmpezarMovimientos(inicioX, inicioY)
    except Exception as e:
        print("Ocurrió un error:", str(e))


frameP = Frame(pantalla, background="WHITE", height=600, width=600, bd=5, relief="solid")
frameP.pack()
frames = []
for x in range(30):
    frame1 = []
    for y in range(30):
        frame1.append(
            Frame(frameP, height=20, width=20))

        frame1[y].grid(row=y, column=x, padx=0, pady=0)
    frames.append(frame1)

Inicio = Button(pantalla, text="Inicio", command=inicio)
Inicio.pack()

# Configurar el listener de eventos del teclado
listener = keyboard.Listener(
    on_press=on_key_press)
listener.start()

pantalla.mainloop()
