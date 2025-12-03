
# Hacer un programa que guarde en una base de datos una clasificacion de animales,
# si son perros voy a guardar nombre edad y raza, si son gatos solo puede guardar 
# nombre y edad, y si es ave, solo nombre edad y tipo de ave.

# PERROS: nombre edad y raza
# GATOS: nombre y edad
# AVES: nombre edad y tipo de ave

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import sqlite3

def crearBaseDatos():
    con = sqlite3.connect("Animales.db")
    cursor = con.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS animales(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            especie TEXT NOT NULL,
            nombre TEXT NOT NULL,
            edad INTEGER NOT NULL,
            raza TEXT,
            tipo_ave TEXT
        )
    """)
    con.commit()
    con.close()

class Principal():
    def __init__(self, master):
        self.ven = master
        self.ven.title('Clasificación de Animales')
        ancho = 600
        alto = 380
        ventana_ancho = self.ven.winfo_screenwidth()
        ventana_alto = self.ven.winfo_screenheight()
        x = (ventana_ancho // 2) - (ancho // 2)
        y = (ventana_alto // 2) - (alto // 2)
        self.ven.geometry(f"{ancho}x{alto}+{x}+{y-80}")

    def inicio(self):
        Label(self.ven, text="Registro de Animales").place(x=10,y=5)

        Label(self.ven, text="Especie").place(x=10,y=30)
        # Combobox (ttk) para elegir la especie: "Perro", "Gato", "Ave"
        self.especie = ttk.Combobox(self.ven, values=("Perro","Gato","Ave"), state="readonly")
        self.especie.place(x=10,y=50)
        self.especie.bind("<<ComboboxSelected>>", self.cambiar_campos)

        Label(self.ven, text="Nombre").place(x=150,y=30)
        self.nombre = Entry(self.ven)
        self.nombre.place(x=150,y=50)

        Label(self.ven, text="Edad").place(x=330,y=30)
        self.edad = Entry(self.ven)
        self.edad.place(x=330,y=50)

        # Campo extra que servirá para 'raza' (perros) o 'tipo de ave' (aves).
        Label(self.ven, text="Raza / Tipo Ave").place(x=430,y=30)
        self.extra = Entry(self.ven)
        self.extra.place(x=430,y=50)

        columnas = ("ID","ESPECIE","NOMBRE","EDAD","EXTRA")
        self.tabla = ttk.Treeview(self.ven, columns=columnas, show="headings")
        self.tabla.place(x=10, y=100, width=560, height=220)
        for col in columnas:
            self.tabla.heading(col, text=col)
            # Ajuste de ancho: ID un poco más pequeño
            if col == "ID":
                self.tabla.column(col, anchor="center", width=40)
            else:
                self.tabla.column(col, anchor="center", width=125)

        scrolly = ttk.Scrollbar(self.ven, orient="vertical", command=self.tabla.yview)
        scrollx = ttk.Scrollbar(self.ven, orient="horizontal", command=self.tabla.xview)
        scrolly.place(x=570, y=100, height=220)
        scrollx.place(x=10, y=320, width=560)

        # botones en la parte inferior
        Button(self.ven, text="Agregar", width=12, command=self.agregar).place(x=80,y=330)
        Button(self.ven, text="Eliminar", width=12, command=self.eliminar).place(x=220,y=330)
        Button(self.ven, text="Limpiar", width=12, command=self.limpiar).place(x=360,y=330)
        Button(self.ven, text="Actualizar tabla", width=12, command=self.actualizartable).place(x=500,y=330)

        # bind para seleccionar fila y cargar en cajas
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionfila)

        # iniciar valores y mostrar la tabla
        self.especie.set("Perro")
        self.cambiar_campos()
        self.actualizartable()

    def cambiar_campos(self, event=None):
        """
        Ajusta el placeholder/etiqueta implícita del campo 'extra' según especie:
        - Perro -> Raza
        - Gato  -> campo extra no aplicable (se deshabilita)
        - Ave   -> Tipo de ave
        """
        esp = self.especie.get()
        if esp == "Perro":
            self.extra.config(state="normal")
            # opcional: limpiar y colocar hint (no hay hint nativo, solo se deja vacío)
            self.extra.delete(0,END)
        elif esp == "Gato":
            # los gatos no usan el campo extra
            self.extra.delete(0,END)
            self.extra.config(state="disabled")
        elif esp == "Ave":
            self.extra.config(state="normal")
            self.extra.delete(0,END)

    def agregar(self):
        esp = self.especie.get()
        nom = self.nombre.get().strip()
        ed = self.edad.get().strip()
        ext = self.extra.get().strip() if self.extra.cget("state") == "normal" else ""

        # validaciones simples
        if not nom or not ed:
            messagebox.showerror("Error","Faltan datos obligatorios (nombre o edad).")
            return
        try:
            ed_i = int(ed)
        except:
            messagebox.showerror("Error","Edad debe ser un número entero.")
            return

        raza = None
        tipo_ave = None
        if esp == "Perro":
            if not ext:
                messagebox.showerror("Error","Para Perro debes indicar la raza.")
                return
            raza = ext
        elif esp == "Ave":
            if not ext:
                messagebox.showerror("Error","Para Ave debes indicar el tipo de ave.")
                return
            tipo_ave = ext
        # Gato no usa campo extra

        con = sqlite3.connect("Animales.db")
        cursor = con.cursor()
        cursor.execute("INSERT INTO animales (especie,nombre,edad,raza,tipo_ave) VALUES (?,?,?,?,?)",
                       (esp, nom, ed_i, raza, tipo_ave))
        con.commit()
        con.close()

        messagebox.showinfo("Listo","Animal agregado correctamente.")
        self.limpiar()
        self.actualizartable()

    def actualizartable(self):
        # vaciar tabla
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        # cargar datos
        con = sqlite3.connect("Animales.db")
        cursor = con.cursor()
        cursor.execute("SELECT id, especie, nombre, edad, raza, tipo_ave FROM animales")
        for fila in cursor.fetchall():
            idf, esp, nom, ed, raza, tipo = fila
            extra = ""
            if esp == "Perro" and raza:
                extra = raza
            elif esp == "Ave" and tipo:
                extra = tipo
            # Gato tendrá extra vacío
            self.tabla.insert("", END, values=(idf, esp, nom, ed, extra))
        con.close()

    def seleccionfila(self, event):
        try:
            index = self.tabla.selection()[0]
        except:
            return
        valores = self.tabla.item(index, "values")
        # valores = (id, especie, nombre, edad, extra)
        self.especie.set(valores[1])
        # asegurarse de que el campo extra tenga el estado correcto
        self.cambiar_campos()
        self.nombre.delete(0,END)
        self.nombre.insert(0, valores[2])
        self.edad.delete(0,END)
        self.edad.insert(0, valores[3])
        if self.extra.cget("state") == "normal":
            self.extra.delete(0,END)
            self.extra.insert(0, valores[4])
        else:
            self.extra.delete(0,END)

    def eliminar(self):
        try:
            index = self.tabla.selection()[0]
        except:
            messagebox.showerror("Error","Selecciona un registro para eliminar.")
            return
        valores = self.tabla.item(index, "values")
        idf = valores[0]
        # eliminar de la BD
        con = sqlite3.connect("Animales.db")
        cursor = con.cursor()
        cursor.execute("DELETE FROM animales WHERE id=?", (idf,))
        # reajustar ids para mantener la numeración como en tus ejemplos
        cursor.execute("UPDATE animales SET id = id - 1 WHERE id > ?", (idf,))
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='animales'")
        con.commit()
        con.close()
        messagebox.showinfo("Listo","Registro eliminado.")
        self.limpiar()
        self.actualizartable()

    def limpiar(self):
        self.nombre.delete(0,END)
        self.edad.delete(0,END)
        # habilitar/limpiar campo extra
        self.extra.config(state="normal")
        self.extra.delete(0,END)
        # dejar especie en Perro por defecto
        self.especie.set("Perro")
        self.cambiar_campos()

if __name__=='__main__':
    crearBaseDatos()
    master = Tk()
    app = Principal(master)
    app.inicio()
    master.mainloop()