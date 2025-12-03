from tkinter import *
from tkinter import messagebox
import sqlite3
from tkinter import ttk
import tkinter as tk
import random

def crearBaseDatos():
    #CREA BASE DE DATOS tienda.db
    con = sqlite3.connect("tienda.db")
    #CURSOR PARA EJECUTAR COMANDOS SQL
    cursor = con.cursor()
    #CREA LA TABLA productos
    cursor.execute("""CREATE TABLE IF NOT EXISTS productos(
                   id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   codigo TEXT NOT NULL,
                   producto TEXT NOT NULL, 
                   precio REAL NOT NULL)""")
    #CREA LA TABLA almacen
    cursor.execute("""CREATE TABLE IF NOT EXISTS almacen(
                   id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   codigoproducto TEXT NOT NULL,
                   stock INTEGER NOT NULL, 
                   descripcion TEXT NOT NULL)""")
    con.commit()
    con.close()


class Principal():
    def __init__(self, master):
        self.ven = master
        self.ven.title('Practica 2 Parcial 3')
        self.ven.geometry("550x400")
        ancho = 550
        alto = 400
        ventana_alto = self.ven.winfo_screenwidth()
        ventana_ancho = self.ven.winfo_screenheight()
        x = (ventana_alto // 2) - (ancho // 2)
        y = (ventana_ancho // 2) - (alto // 2)
        self.ven.geometry(f"{ancho}x{alto}+{x}+{y-100}")
        #ELIMINAR UN REGISTRO
        self.index = -1

        
    def inicio(self):
        self.us=Label(self.ven, text=f"CRUD DE PRODUCTOS")
        self.us.place(x=50,y=5)
        Label(self.ven, text="Producto").place(y=30,x=10)
        self.producto = Entry(self.ven)
        self.producto.place(y=50,x=10)
        Label(self.ven, text="Descripcion").place(y=30,x=150)
        self.descripcion = Entry(self.ven)
        self.descripcion.place(y=50,x=150)
        Label(self.ven, text="Precio").place(y=30,x=290)
        self.precio = Entry(self.ven)
        self.precio.place(y=50,x=290)
        Label(self.ven, text="Cantidad").place(y=30,x=420)
        self.cantidad = Entry(self.ven)
        self.cantidad.place(y=50,x=420)
        #TITULOS DE LA TABLA CREADA 
        columnas = ("ID","CODIGO","PRODUCTO","PRECIO","DESCRIPCION","STOCK")
        #CREAR EL TREEVIEW
        self.tabla = ttk.Treeview(self.ven, columns= columnas, show="headings")
        self.tabla.place(x=10, y=100, width=480,height=190)

        #MUESTRA TEXTO DEL ENCABEZADO IMPORTANTE
        for col in columnas:
            self.tabla.heading(col,text=col)
            self.tabla.column(col, anchor="center", width=30)
        #CREA BARRAS PARA DESPLAZARSE
        scrolly = ttk.Scrollbar(self.ven,orient="vertical", command=self.tabla.yview)
        scrollx = ttk.Scrollbar(self.ven, orient="horizontal", command=self.tabla.xview)
        scrolly.place(x=480,y=90,height=200)
        scrollx.place(x=10,y=280, width=470)

        self.agregar = Button(self.ven, text="Agregar", width=10, state="normal", command=self.agregarproducto)
        self.agregar.place(x=30,y=320)

        self.modificar = Button(self.ven, text="Modificar", width=10, state="disabled", command=self.modificarproducto)
        self.modificar.place(x=120,y=320)

        self.eliminar = Button(self.ven, text="Eliminar", width=10, state="disabled", command=self.eliminarproducto)
        self.eliminar.place(x=210,y=320)
        
        #SELECCIONAR UNA FILA
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionfila)
        #TRAE LOS DATOS DE LA BASE DE DATOS PARA AGREGARLOS AL TREEVIEW
        self.mostrarDatos()


    def modificarproducto(self):
        #OBTENER LA FILA SELECCIONADA EN LA TABLA 
        try:
            self.index = self.tabla.selection()[0]
        except:
            return
        #RECUPERA LOS VALORES DE LA FILA SELECCIONADA 
        valores = self.tabla.item(self.index,"values")
        #IDENTIFICADOR DEL PRODUCTO QUESE VA A MODIFICAR
        id = valores[0]
        #OBTIENE LOS DATOS INGRESADOS POR EL USUARIO EN LAS CAJAS DE TEXTO
        pro = self.producto.get()
        pre = self.precio.get()
        des = self.descripcion.get()
        can = self.cantidad.get()
        #VERIFICA QUE NO TENGA CAJAS VACIAS 
        if len(pro) != 0 and len(pre) != 0 and len(des)!= 0 and len(can)!= 0:
            codigo = pro[:2].upper() + str(random.randint(0,100)) + des[0].upper()
            #GENERA CODIGO: PRIMERAS 2 LETRAS DEL NOMBRE 
            #               NUMERO ALEATORIO ENTRE 0 Y 100 
            #               PRIMERA LETRA DE LA DESCRIPCION 
            #CONECTA CON LA BASE DE DATOS
            con = sqlite3.connect("tienda.db")
            cursor = con.cursor()
            #ACTUALIZA LOS DATOS DEL PRODUCTO EN PRODUCTO Y ALMACEN
            cursor.execute("UPDATE productos SET codigo=?, producto=?, precio=? WHERE id=?",(codigo,pro,pre,id))
            cursor.execute("UPDATE almacen SET codigoproducto=?, stock=?, descripcion=? WHERE id=?",(codigo,can,des,id))
            
            con.commit()
            con.close()
            self.limpiarcajas()
            self.actulizartable()
            #ACTIVA Y DESACTIVA LOS BOTONES 
            self.agregar.config(state="normal")
            self.modificar.config(state="disabled")
            self.eliminar.config(state="disabled")
        else:
            messagebox.showinfo("Erro","Faltan datos")

    def eliminarproducto(self):
        try:
            self.index = self.tabla.selection()[0]
        except:
            return
        
        valores = self.tabla.item(self.index,"values")
        id = valores[0]

        con = sqlite3.connect("tienda.db")
        cursor = con.cursor()

        cursor.execute("DELETE FROM productos WHERE id=?",(id))
        cursor.execute("DELETE FROM almacen WHERE id=?",(id))
       
        con.commit()
        con.close()
        self.actulizartable()
        self.limpiarcajas()

        self.agregar.config(state="normal")
        self.modificar.config(state="disabled")
        self.eliminar.config(state="disabled")

    def seleccionfila(self, event):
        self.limpiarcajas()
        try:
            self.index = self.tabla.selection()[0]
        except:
            return
        valores = self.tabla.item(self.index,"values")

        self.producto.insert(0,valores[2])
        self.precio.insert(0,valores[3])
        self.descripcion.insert(0,valores[4])
        self.cantidad.insert(0,valores[5])

        self.agregar.config(state="disabled")
        self.modificar.config(state="normal")
        self.eliminar.config(state="normal")

    def mostrarDatos(self):
        con = sqlite3.connect("tienda.db")
        cursor = con.cursor()
        cursor.execute("""
            SELECT productos.id,
                    productos.codigo,
                    productos.producto,
                    productos.precio,
                    almacen.descripcion,
                    almacen.stock
            FROM productos
            INNER JOIN almacen
            ON productos.codigo = almacen.codigoproducto
        """
        )
        
        for i in cursor.fetchall():
            self.tabla.insert("",END,values=i)
        con.commit()
        con.close()
    
    def verificar(self):
        p = self.producto.get()
        d = self.descripcion.get()
        pr = self.precio.get()
        s = self.cantidad.get()

        if len(p)!=0 and len(d)!=0 and len(pr)!= 0 and len(s)!= 0:
            con = sqlite3.connect("tienda.db")
            cursor = con.cursor()
            #ABRE BASE DE DATOS Y EJECUTA UNA CONSULTA PARA BUSCAR 
            #EL PRODUCTO QUE TENGA EL MISMO NOMBRE Y DESCRIPCION
            cursor.execute("""
                SELECT productos.*, almacen.*
                FROM productos
                JOIN almacen ON productos.codigo = almacen.codigoproducto
                WHERE productos.producto = ? AND almacen.descripcion = ?
            """, (p, d))
            #DEVUELVE LA PRIMERA COINCIDENCIA ENCONTRANDO NONE SI NO EXISTE
            resultado = cursor.fetchone()
            con.commit()
            cursor.close()
            print(resultado)
            if not resultado:
                return False
            else:
                return resultado[0]

    def agregarproducto(self):
        #REVISA SI YA EXISTE UN PRODUCTO CON EL MISMO NOMBRE
        if self.verificar():
            id = self.verificar()
            print(id)

            p = self.producto.get()
            d = self.descripcion.get()
            pr = self.precio.get()
            s = self.cantidad.get()

            if len(p)!=0 and len(d)!=0 and len(pr)!= 0 and len(s)!= 0:
                con = sqlite3.connect("tienda.db")
                cursor = con.cursor()
                #ACTUALIZA PRECIO (PRODUCTOS) Y STOCK (ALMACEN)
                cursor.execute("UPDATE productos SET precio=? WHERE producto=?",(pr,p))
                cursor.execute("UPDATE almacen SET stock=? WHERE descripcion=?",(s,d))
                
                con.commit()
                con.close()
                self.limpiarcajas()
                self.actulizartable()
        else:
            #CONCIERTE PRECIO FLOAT Y CANTIDAD ENTERO
            prf = 0.0
            st = 0

            p = self.producto.get()
            d = self.descripcion.get()
            pr = self.precio.get()
            s = self.cantidad.get()

            if len(p)!=0 and len(d)!=0 and len(pr)!= 0 and len(s)!= 0:
                prf = float(pr)
                st = int(s)
                #GENERA CODIGO ALEATORIO PARA EL PRODUCTO 
                codigo = p[:2].upper() + str(random.randint(0,100)) + d[0].upper()  
                con = sqlite3.connect("tienda.db")
                cursor = con.cursor()
                #INSERTA LOS DATOS EN LAS TABLAS 
                cursor.execute("INSERT INTO productos (codigo,producto,precio) VALUES (?,?,?)",(codigo, p,prf))
                cursor.execute("INSERT INTO almacen (codigoproducto,descripcion,stock) VALUES (?,?,?)",(codigo,d,st))
                con.commit()
                con.close()
                self.actulizartable()
                self.limpiarcajas()
            else:
                messagebox.showerror("ERROR","Faltan datos")

    def limpiarcajas(self):
        self.producto.delete(0,END)
        self.precio.delete(0,END)
        self.descripcion.delete(0,END)
        self.cantidad.delete(0,END)

    def actulizartable(self):
        for i in self.tabla.get_children():
                self.tabla.delete(i)
        self.mostrarDatos()


if __name__=='__main__':
    crearBaseDatos()
    master = Tk()
    app = Principal(master)
    app.inicio()
    master.mainloop()
