import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO
from urllib.request import urlopen
import requests
from json import loads
from os import system
system('cls')

# Ventana principal
def VentanaPrincipal():
    ventana = tk.Tk()
    portadaPrincipal = Portada(ventana)
    ventana.mainloop()

# Portada de la interfaz
class Portada():
    def __init__(self, ventana):
        # Diseño de ventana
        self.ventana = ventana
        self.ventana.title('Portal de cédulas')
        self.ventana.iconbitmap('imagenes\iconotk.ico')
        self.ventana.geometry('1260x700')
        self.ventana.resizable(0,0)

        # Imagen de fondo
        self.imagen = tk.PhotoImage(file = r'imagenes\\fondotk.png')
        self.fondoImagen = tk.Label(self.ventana, image = self.imagen)
        self.fondoImagen.place(x = 0, y = 0, relwidth = 1, relheight = 1)

 
        # Botón para acceder al portal
        self.botonAcceso = tk.Button(self.ventana, text = 'Ingrese aquí', width = 20, height = 3, borderwidth = 4, highlightbackground = 'white', font = ('Italic', 15),fg = 'white', background = 'black', activebackground = 'navy',activeforeground = 'white',cursor = 'circle')
        self.botonAcceso.place(x = 525, y = 300)
        self.botonAcceso.config(command = self.clickBotonAcceso)

    #-------------------------------METODOS-------------------------------

    # Nueva ventana
    def NuevaVentana(self):
        self.ventana.withdraw() # Para cerrar ventana anterior
        self.n_ventana2 = Portal() # Objeto que abrirá la nueva ventana

    # Método de carga
    def clickBotonAcceso(self):
        self.carga = tk.Label(self.ventana, text = 'Ingresando al portal...', fg = 'navy', background = 'grey99', font = ('Italic', 13, 'bold'))
        self.carga.place(x = 555, y = 420)
        self.carga.after(1000, self.NuevaVentana)

# Segunda ventana
class Portal():
    def __init__(self):
        self.ventana2 = tk.Toplevel() 
        self.ventana2.title('Portal')
        self.ventana2.iconbitmap(r'imagenes\\IconoVentana2.ico')
        self.ventana2.geometry('1260x700')
        self.ventana2.resizable(0,0)

if __name__ == '__main__':
    VentanaPrincipal()