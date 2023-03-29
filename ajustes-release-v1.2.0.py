# Ultimos ajustes: Visualización de imagen del usuario
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO
from urllib.request import urlopen
import requests
from json import loads
from datetime import date
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

        # Fondo
        self.imagen = tk.PhotoImage(file = r'imagenes\\FondoVentana2.png')
        self.fondo2 = tk.Label(self.ventana2, image = self.imagen)
        self.fondo2.place(x = 0, y = 0, relwidth = 1, relheight = 1)
        

        # Cuadro de texto
        self.textoEntrada = tk.Entry(self.ventana2,foreground = 'black', font = ('Georgia', 14), background = 'lightskyblue3')
        self.textoEntrada.place(x = 650, y = 250, height = 40)

        # Botón de acceso (imagen)
        self.textoBoton = tk.Button(self.ventana2, text = 'Acceder →', font = ('Italic', 13, 'bold'), background = 'gray5', fg = 'white', activebackground = 'navy', activeforeground = 'white', cursor = 'circle')
        self.textoBoton.place(x = 900, y = 250, height = 40)
        self.textoBoton.config(command = self.DatosJson) 

    #------------------------METODOS----------------------

    def DatosJson(self):
        self.data = self.textoEntrada.get()
        # URL para cargar datos
        self.url = f'https://api.adamix.net/apec/cedula/{str(self.data)}'
        self.respuesta = urlopen(self.url)
        self.lectura = self.respuesta.read()

        # URL para cargar imagen
        self.urlImg = requests.get(f'https://api.adamix.net/apec/foto2/{str(self.data)}')
        self.respuestaImg = self.urlImg.content

        self.datos = loads(self.lectura)
            
        # Si la cédula se encuentra disponible, se abre la otra ventana. De lo contrario saldrá un mensaje de error
        if self.datos['ok'] == False:
            messagebox.showerror('Error', 'Cédula no disponible')

        elif self.datos['ok'] == True:
            self.ventana2.withdraw()
            self.n_ventana3 = Datos()

            # Datos extraídos de la API
            self.id = self.datos['Cedula']
            self.nombre = self.datos['Nombres'].capitalize()
            self.apellido = str(self.datos['Apellido1']).capitalize() + ' ' + str(self.datos['Apellido2']).capitalize()
            self.fechaNacimiento = self.datos['FechaNacimiento'].replace('00:00:00.000', ' ')

            # Calculo de la edad del usuario
            self.year = int(self.datos['FechaNacimiento'][0:4])
            self.mes = int(self.datos['FechaNacimiento'][5:7])
            self.dia = int(self.datos['FechaNacimiento'][8:10])
            self.fechas = date(self.year, self.mes, self.dia)
            self.rest_fechas = date.today() - self.fechas
            self.dias = self.rest_fechas.days / 365
            self.edad = int(self.dias)

            self.genero = self.datos['IdSexo']
            self.c_anterior = self.datos['CedulaAnterior']

            # Lectura de imagen
            self.imagenUsuario = Image.open(BytesIO(self.respuestaImg))
            self.imagenUsuario = self.imagenUsuario.resize((100, 100))
            self.foto = ImageTk.PhotoImage(self.imagenUsuario)

            self.n_ventana3.cedula.config(text = f'Cédula: {self.id}')
            self.n_ventana3.nombre.config(text = f'Nombre: {self.nombre}')
            self.n_ventana3.apellido.config(text = f'Apellido: {self.apellido}')
            self.n_ventana3.f_nacimiento.config(text = f'Fecha de nacimiento: {self.fechaNacimiento}')
            self.n_ventana3.genero.config(text = f'Sexo: {self.genero}')
            self.n_ventana3.edad.config(text = f'Edad: {self.edad}')
            self.n_ventana3.c_anterior.config(text = f'Cédula anterior: {self.c_anterior}')
            self.n_ventana3.fotoUsario.config(image = self.foto)


        else:
            messagebox.showwarning('Error', 'Vuelva a intentarlo')

class Datos():
    def __init__(self):
        self.ventana3 = tk.Toplevel()
        self.ventana3.title('Datos del usuario')
        self.ventana3.iconbitmap(r'imagenes\\IconoVentana3.ico')
        self.ventana3.geometry('1260x700')
        self.ventana3.resizable(0,0)

        #fondo  
        self.imagen = tk.PhotoImage(file = r'imagenes\\FondoVentana3.png')
        self.fondo3 = tk.Label(self.ventana3, image = self.imagen)
        self.fondo3.place(x = 0, y = 0, relwidth = 1, relheight = 1)

        # ------------------------DATOS----------------------------------
        # IMAGEN
        self.fotoUsario = tk.Label(self.ventana3)
        self.fotoUsario.place(x = 200, y = 188, width = 250, height = 275)
    
        # Cedula
        self.cedula = tk.Label(self.ventana3, fg = 'navy', font = ('Italic', 16, 'bold'), background = 'white')
        self.cedula.place(x = 500, y = 190)

        # Nombre
        self.nombre = tk.Label(self.ventana3, text = 'Nombre: ', fg = 'navy', font = ('Italic', 16, 'bold'), background = 'white')
        self.nombre.place(x = 500, y = 230)

        # Apellido
        self.apellido = tk.Label(self.ventana3, text = 'Apellido: ', fg = 'navy', font = ('Italic', 16, 'bold'), background = 'white')
        self.apellido.place(x = 500, y = 270)

        # Fecha de nacimiento
        self.f_nacimiento = tk.Label(self.ventana3, text = 'Fecha de nacimiento: ', fg = 'navy', font = ('Italic', 16, 'bold'), background = 'white')
        self.f_nacimiento.place(x = 500, y = 310)

        # Género
        self.genero = tk.Label(self.ventana3, text = 'Sexo: ', fg = 'navy', font = ('Italic', 16, 'bold'), background = 'white')
        self.genero.place(x = 500, y = 350)

        # Edad
        self.edad = tk.Label(self.ventana3, text = 'Edad: ', fg = 'navy', font = ('Italic', 16, 'bold'), background = 'white')
        self.edad.place(x = 500, y = 390)

        # Cedula anterior
        self.c_anterior = tk.Label(self.ventana3, text = 'Cédula anterior: ', fg = 'navy', font = ('Italic', 16, 'bold'), background = 'white')
        self.c_anterior.place(x = 500, y = 430)

        # Botón para retroceder a la ventana anterior
        self.BotonRetroceder = tk.Button(self.ventana3, text = '⮌', fg = 'white', background = 'midnight blue', activebackground = 'black', activeforeground = 'white', font = ('Italic', 12, 'bold'), cursor = 'circle')
        self.BotonRetroceder.place(x = 1010, y = 522, width = 50)
        self.BotonRetroceder.config(command =  self.retroceder)

    # -----------------METODOS-----------------------
    def retroceder(self):
        self.ventana3.withdraw()
        self.retrocederVentana = Portal()

if __name__ == '__main__':
    VentanaPrincipal()