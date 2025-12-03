'''
hacer un programa en tkinter que en una ventana mediante
una caja de texto lea un numero, ese numero se enviara a
otra ventana donde en un lisbiu, mostrara ese numero, el numero de veces
'''

from tkinter import *
from tkinter import messagebox
from tkinter import ttk


class Principal():
    def __init__(self, master):
        self.vetana = master 
        self.vetana.title("Practica  1 Parcial 3")  
        ancho_vetanatana  = 250  
        alto_vetanatana = 200  
        ancho_pantalla = self.vetana.winfo_screenwidth()
        alto_pantalla = self.vetana.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho_vetanatana // 2)
        y = (alto_pantalla // 2) - (alto_vetanatana // 2)
        self.vetana.geometry(f"{ancho_vetanatana}x{alto_vetanatana}+{x}+{y}")
    
    def inicio(self):
        Label(self.vetana, text = "Numero: ").place(x = 100, y = 50)
        self.nume1 = Entry(self.vetana)
        self.nume1.place(x = 60, y = 100)
        Button(self.vetana, text = "Enviar", command = self.enviar).place(x = 100, y = 150)
        Button(self.vetana, text = "Salir", command = self.destruir).place(x = 200, y = 150)

    def enviar(self):
        try:
            if len(self.nume1.get()) <= 0:
                messagebox.showerror("Error", "Campo vacio")
                return 1
            
            numero = int(self.nume1.get())
            self.nume1.delete(0, END)
            self.vetana.withdraw() 
            nuevaVen = Toplevel(self.vetana)
            Ventana_lista(nuevaVen, self.vetana, numero)

        except ValueError: 
            messagebox.showerror("Error", "No son numeros")
            self
    
    def destruir(self):
        self.vetana.destroy()

class Ventana_lista():
    def __init__(self, master,vetana, dato):
        self.ventaPrimaria = vetana
        self.numero = dato
        self.vetnanaSec = master
        self.vetnanaSec.title("Resultado de numero")  
        ancho_vetanatana  = 250  
        alto_vetanatana = 200 
        ancho_pantalla = self.vetnanaSec.winfo_screenwidth()
        alto_pantalla = self.vetnanaSec.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho_vetanatana // 2)
        y = (alto_pantalla // 2) - (alto_vetanatana // 2)
        self.vetnanaSec.geometry(f"{ancho_vetanatana}x{alto_vetanatana}+{x}+{y}")
        
        self.inicio()
    
    def inicio(self):
        Label(self.vetnanaSec, text = "Resultados de la Operacion").place(x = 50, y = 10)
        self.miLista = Listbox(self.vetnanaSec, height = 10, width = 8, bg = "white")
        self.miLista.place(x = 80, y = 30)
        Button(self.vetnanaSec, text = "Regresar", command = self.volver).place(x = 10, y = 50)
        self.ingresarDatos()

    def ingresarDatos(self):
        for i in range(self.numero):
            self.miLista.insert(END, self.numero) 

    def volver(self):
        self.vetnanaSec.destroy()
        self.ventaPrimaria.deiconify()

if __name__ == "__main__":
    master = Tk()
    app = Principal(master)
    app.inicio()
    master.mainloop()