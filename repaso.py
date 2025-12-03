from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import sqlite3
import random

#CREACION DE BASE DE DATOS
def crearBaseDatos():
    #CONEXION A LA BASE DE DATOS LLAMADA ALUMNOS.DB
    con = sqlite3.connect("Alumnos.db")
    #ESCRIBIR COMANDOS SQL
    cursor = con.cursor()
    #CREACION DE LA TABLA LLAMADA ALUMNO
    cursor.execute("""CREATE TABLE IF NOT EXISTS alumno(
                   id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   nombre TEXT NOT NULL,
                   edad INTEGER NOT NULL, 
                   carrera TEXT NOT NULL)""")
    #GUARDA CAMBIOS 
    con.commit()
    #CERRAR LA BASE DE DATOS PARA NO DEJARLA HABIERTA
    con.close()

class Principal():
    #CREA TITULO Y TAMAÑO DE VENTANA
    def __init__(self, master):
        self.ventana = master 
        self.ventana.title("REPASO")    
        ancho_ventana  = 600 
        alto_ventana= 400  
        ancho_pantalla = self.ventana.winfo_screenwidth()
        alto_pantalla = self.ventana.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)
        self.ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

        #PARA ELIMINAR UN ALUMNO 
        self.index = -1

    def inicio(self):
        #ETIQUETA
        Label(self.ventana, text = "Nombre").place(x = 80, y = 20)
        #CAJA DE TEXTO
        self.nombre = Entry(self.ventana)
        self.nombre.place(x = 50, y = 50)

        #ETIQUETA
        Label(self.ventana, text = "Edad").place(x = 245, y = 20)
        #CAJA DE TEXTO
        self.edad = Entry(self.ventana)
        self.edad.place(x = 200, y = 50)

        #ETIQUETA
        Label(self.ventana, text = "Carrera").place(x = 375, y = 20)
        #CAJA DE TEXTO
        self.carrera = Entry(self.ventana)
        self.carrera.place(x = 340, y = 50)

        #BOTON
        self.agregar = Button(self.ventana, text="Agregar", width=10, state="normal", command=self.agregaralumno)
        self.agregar.place(x=10,y=320)

        self.modificar = Button(self.ventana, text="Modificar", width=10, state="normal", command=self.modificaralumno)
        self.modificar.place(x=100,y=320)

        self.eliminar = Button(self.ventana, text="Eliminar", width=10, state="normal", command=self.eliminaralumno)
        self.eliminar.place(x=190,y=320)
        
        #TREEVIEW
        #NOMBRES DE LAS COLUMNAS DE LA TABLA 
        columnas = ("ID","NOMBRE","EDAD","CARRERA")
        #CREAR EL TREEVIEW
        self.tabla = ttk.Treeview(self.ventana, columns= columnas, show="headings")
        self.tabla.place(x=10, y=100, width=480,height=190)
        
        #MUESTRA TEXTO DEL ENCABEZADO IMPORTANTE
        for col in columnas:
            self.tabla.heading(col,text=col)
            self.tabla.column(col, anchor="center", width=30)
        #CREA BARRAS PARA DESPLAZARSE
        scrolly = ttk.Scrollbar(self.ventana,orient="vertical", command=self.tabla.yview)
        scrollx = ttk.Scrollbar(self.ventana, orient="horizontal", command=self.tabla.xview)
        scrolly.place(x=480,y=90,height=200)
        scrollx.place(x=10,y=280, width=470)

        #SELECCIONAR UNA FILA
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionfila)
        #TRAE LOS DATOS DE LA BASE DE DATOS PARA AGREGARLOS AL TREEVIEW
        self.mostrarDatos()

    def agregaralumno(self):
        #CAJAS DE TEXTO MANDAS A LLAMAR
        n = self.nombre.get()
        e = self.edad.get()
        c = self.carrera.get()
        #VERIFICAN SI ESTAN VACIAS
        if len(n)!=0 and len(e)!=0 and len(c)!= 0:
            #CONECTAR A LA BASE DE DATOS
            con = sqlite3.connect("Alumnos.db")
            cursor = con.cursor()
            #INSERTAR DATOS EN LA TABLA
            cursor.execute("INSERT INTO alumno (nombre, edad, carrera) VALUES (?, ?, ?)",
            (n, e, c))
            #GUARDA REGISTRO
            con.commit()
            #CIERRA LA CONEXION
            con.close()
            #ACTUALIZAR LA TABLA
            self.actualizartabla()
        #ERROR SI ALGUNA CAJA ESTA VACIA
        else:
            messagebox.showerror("ERROR","Faltan datos")    
            

    def modificaralumno(self):
        #VERIFICAR SI SE SELECCIONO UNA FILA EN LA TABLA
        try:
            self.index = self.tabla.selection()[0]
        except:
            messagebox.showerror("Error", "Selecciona un registro para modificar")
            return
        #OBTIENE LOS VALORES DE ESA FILA
        valores = self.tabla.item(self.index,"values")
        #GUARDA EL ID DEL ALUMNO SELECCIONADO
        id = valores[0]
        #OBTIENE LO QUE EL USUARIO ESCRIBIO Y ACTUALIZO
        n = self.nombre.get()
        e = self.edad.get()
        c = self.carrera.get()
        
        #CAJAS NO VACIAS
        if len(n) != 0 and len(e) != 0 and len(c)!= 0:
            #CONEXION A LA BASE DE DATOS
            con = sqlite3.connect("Alumnos.db")
            cursor = con.cursor()
            #ACTUALIZA EL REGISTRO EN LA BASE DE DATOS
            cursor.execute("UPDATE alumno SET nombre=?, edad=?, carrera=? WHERE id=?",(n,e,c,id))
            #UPDATE: TABLA SET: CAMBIAR CAMPOS WHERE=REGISTRO DE ESA ID 
            con.commit()
            con.close()
            self.limpiarcajas()
            self.actualizartabla()
            #ACTIVA BOTON AGREGAR, DESACTIVA BOTON MODIFICAR Y ELIMINAR
            self.agregar.config(state="normal")
            self.modificar.config(state="disabled")
            self.eliminar.config(state="disabled")

            messagebox.showinfo("Éxito", "Alumno modificado correctamente")
        else:
            messagebox.showerror("Error","Faltan datos")

    def eliminaralumno(self):
        #VERIFICAR SI SE SELECCIONO UNA FILA EN LA TABLA
        try:
            self.index = self.tabla.selection()[0]
        except:
            return
        #OBTIENE LOS VALORES DE LA FILA SELECCIONADA
        valores = self.tabla.item(self.index,"values")
        #EXTRAE EL ID DEL ALUMNO A ELIMINAR
        id = valores[0]
        #CONECTA CON LA BASE DE DATOS
        con = sqlite3.connect("Alumnos.db")
        cursor = con.cursor()
        #EJECUTA EL COMANDO PARA ELIMINAR EL REGISTRO
        cursor.execute("DELETE FROM alumno WHERE id=?",(id,))
        #GUARDA LOS CAMBIOS Y CIERRA
        con.commit()
        con.close()
        self.actualizartabla()
        self.limpiarcajas()

        #HABILITA AGREGAR, DESHABILITA MODIFICAR Y ELIMINAR
        self.agregar.config(state="normal")
        self.modificar.config(state="disabled")
        self.eliminar.config(state="disabled")
    
    #ACTUALIZAR LA TABLA CUANDO AGREGA UN DATO
    def actualizartabla(self):
        #LIMPIA LA TABLA COMPLETA
        for i in self.tabla.get_children():
                self.tabla.delete(i)
        #CONECTA BASE DE DATOS, SELECT DEL ALUMNO E INSERTAR REGISTRO EN TREEVIEW
        self.mostrarDatos()
        "SIRVE PARA ACTUALIZAR TABLA DESPUES DE AGREGAR, MODIFICAR Y ELIMINAR"
 
    #MOSTRAR LOS DATOS EN LA TABLA
    def mostrarDatos(self):
        #CONECTAR A LA BASE DE DATOS
        con = sqlite3.connect("Alumnos.db")
        cursor = con.cursor()
        #SELECCIONAR LOS DATOS DE LA TABLA
        cursor.execute("""
            SELECT id, nombre, edad, carrera FROM alumno
        """
        )
        #LIMPIA LA TABLA ANTES DE MOSTRAR LOS DATOS
        for fila in self.tabla.get_children():
           self.tabla.delete(fila)
        #INSERTA LOS DATOS DE LA BASE EN EL TREEVIEW
        for i in cursor.fetchall():
            self.tabla.insert("",END,values=i)

        con.commit()
        con.close()
    
    def seleccionfila(self, event):
        #BORRA LO ECRITO ANTERIORMENTE 
        self.limpiarcajas()
        #SELECCIONAR LA FILA
        try:
            self.index = self.tabla.selection()[0]
        except:
            return
        #OBTIENE LOS VALORES DE ESA FILA
        valores = self.tabla.item(self.index,"values")
        #COLOCA ESOS VALORES EN LAS CAJAS DE TEXTO
        self.nombre.insert(0,valores[1])
        self.edad.insert(0,valores[2])
        self.carrera.insert(0,valores[3])
        
        self.agregar.config(state="disabled")
        self.modificar.config(state="normal")
        self.eliminar.config(state="normal")
    
    def limpiarcajas(self):
        self.nombre.delete(0,END)
        self.edad.delete(0,END)
        self.carrera.delete(0,END)
        

if __name__ == "__main__":
    crearBaseDatos()
    master = Tk()
    app = Principal(master)
    app.inicio()
    master.mainloop()