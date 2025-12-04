#LIBRERIAS/LIBRARIES
from tkinter import *
from tkinter import messagebox

#CLASE PRINCIPAL/MAIN CLASS
class Principal():
     
    #TAMAÑO DE LA VENTANA /WINDOW SIZE
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

    #INTERFAZ DE LA VENTANA/WINDOW INTERFACE  
    def inicio(self):  
        Label(self.vetana, text = "Escribe un numero: ").place(x = 20, y = 20)
        self.n1 = Entry(self.vetana)
        self.n1.place(x = 50, y = 50)
       
        Label(self.vetana, text= "Escribe un numero ").place(x = 20, y = 75)
        self.n2 = Entry(self.vetana)
        self.n2.place(x = 50, y = 100)
        
        Button(self.vetana, text = "Enviar", width=15, command= self.enviar).place(x = 50, y = 130)
        Button(self.vetana, text = "Cerrar", width=15, command= self.cerrar).place(x = 50, y = 160)

        self.vetana.mainloop()

    def enviar(self):
        try:
            #OBTIENE LOS VALORES DE LAS CAJAS DE TEXTO
            #GET THE VALUES FROM THE TEXTBOXES
            "SOLO PERMITE NUMEROS POR (INT)"
            caja1 = int(self.n1.get())
            caja2 = int(self.n2.get())
            #LIMPIA LAS CAJAS
            #CLEARS THE TEXTBOXES
            self.n1.delete(0, END)
            self.n2.delete(0, END)
            #OCULTA VENTANA 1 (PRINCIPAL)
            #HIDES MAIN WINDOW
            self.vetana.withdraw() 
            #CREACION VENTANA 2
            #CREATES WINDOW 2
            otra = Toplevel(self.vetana)
            #ABRE LA CLASE DE LA VENTANA 2
            #OPENS THE CLASS FOR WINDOW 2
            Ventana2(otra, self.vetana, caja1, caja2) 

        except ValueError:
            messagebox.showerror("Error", "Algun dato no es numero")
            
            self.n1.delete(0, END)
            self.n2.delete(0, END)
    
    #CIERRA COMPLETAMENTE VENTANA 1 AL PRESIONAR BOTON SALIR
    #CLOSES MAIN WINDOW COMPLETELY WHEN PRESSING EXIT BUTTON
    def cerrar(self):
        self.vetana.destroy()
#VENTANA 2/WINDOW 2
class Ventana2 ():
    def __init__(self, master,vetana, c1, c2):
        self.venDos = master
        self.venDos.title("Practica  1 Parcial 3") 
        ancho_vetanatana  = 250 
        alto_vetanatana = 200  
        ancho_pantalla = self.venDos.winfo_screenwidth()
        alto_pantalla = self.venDos.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho_vetanatana // 2)
        y = (alto_pantalla // 2) - (alto_vetanatana // 2)
        self.venDos.geometry(f"{ancho_vetanatana}x{alto_vetanatana}+{x}+{y}")

        Label(self.venDos, text = "Hola mundo").place(x = 50, y = 20)

        Button(self.venDos, text = "Regresar",width=10, command= self.regresar).place(x = 50, y = 100)
        Button(self.venDos, text = "Sumar",width=10, command= self.sumar).place(x = 50, y = 50)
        #GUARDA LOS VALORES ENVIADOS
        #SAVES THE RECEIVED VALUES
        self.vetana = vetana
        self.c1 = c1
        self.c2 = c2

    def regresar(self):
        #CIERRA VENTANA 2/CLOSES WINDOW 2 
        self.venDos.destroy()
        #VUELVE A MOSTRAR VENTANA 1/SHOWS WINDOW 1 AGAIN
        self.vetana.deiconify()
    
    #SUMA DE LOS DOS NUMEROS QUE MUESTRA EN UN MENSAJE 
    #SUMS THE TWO NUMBERS AND SHOWS THEM IN A MESSAGEBOX
    def sumar(self):
        messagebox.showinfo("Suma", f"La suma  de {self.c1} y {self.c2} es: {self.c1 + self.c2}")


if __name__ == "__main__":
    master = Tk()
    app = Principal(master)
    app.inicio()
    master.mainloop()