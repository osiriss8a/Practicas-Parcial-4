from tkinter import * 
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import sqlite3

#CREACION BASE DE DATOS
def crearBaseDatos():
    #CONECTAR BASE DE DATOS LLAMDA Usuarios.db
    con = sqlite3.connect("Usuarios.db")
    cursor = con.cursor()
    #CREA LA TABLA 
    cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL,password TEXT NOT NULL)""")
    #VERIFICA SI EXISTE EL USUARIO "admin"
    cursor.execute("SELECT * FROM usuarios WHERE usuario='admin'")
    #FETOCHE DEVUELVE REGISTRO NONE, SI NO EXISTE ENTRA AL IF
    if not cursor.fetchone():
        #INSERTA USUARIO POR DEFECTO
        cursor.execute("INSERT INTO usuarios (usuario,password) VALUES (?,?)",("admin","12345"))
    #GUARDA CAMBIOS Y CERRAR
    con.commit()
    con.close()

class Ventana():
    def __init__(self,master):
        self.ven = master
        self.ven.title('Programa 2')
        ancho = 250
        alto = 200
        ventana_ancho = self.ven.winfo_screenwidth()
        ventana_alto = self.ven.winfo_screenheight()
        x = (ventana_ancho // 2) - (ancho // 2)
        y = (ventana_alto // 2) - (alto // 2)
        self.ven.geometry(f'{ancho}x{alto}+{x}+{y}')

    def Inicio(self):
        Label(self.ven,text='Usuario').place(x=50,y=20)
        self.n1 = Entry(self.ven)
        self.n1.place(x=50,y=50)

        Label(self.ven,text='Password').place(x=50,y=75)
        self.n2 = Entry(self.ven, show="*")
        self.n2.place(x=50,y=100)

        Button(self.ven,text='Validar',command=self.Enviar,width=10,fg='green').place(x=30,y=140)
        Button(self.ven,text='Cerrar',command=self.Cerrar,width=10,fg='red').place(x=150,y=140)

    def Enviar(self):
        #OBTIENE LOS DATOS DE LAS CAJAS DE TEXTO
        u = self.n1.get()
        p = self.n2.get()
        #CONECTA CON LA BASE DE DATOS
        con = sqlite3.connect("Usuarios.db")
        cursor = con.cursor()
        #VERIFICA SI EXISTE EL USUARIO
        cursor.execute("SELECT * FROM usuarios WHERE usuario=? and password=?", (u,p))
        #OBTIENE EL RESULTADO
        resultado = cursor.fetchone()
        #CIERRA LA CONEXION
        con.close()
        #SI EL RESULTADO SE ENCUENTRA ENTONCES..
        if resultado:
            #LIMPIA CAJAS DE TEXTO
            self.n1.delete(0,END)
            self.n2.delete(0,END)
            #OCULTA LA VENTANA 1
            self.ven.withdraw()
            #CREA VENTANA 2
            otra = Toplevel(self.ven)
            #ABRE LA VENTANA 2
            Ventanados(otra,self.ven,u)
        else:
            messagebox.showerror('Error','Datos incorrectos')
            self.n1.delete(0,END)
            self.n2.delete(0,END)
            
    #CIERRA TOTALMENTE LAS VENTANAS CON BOTON SALIR
    def Cerrar(self):
        self.ven.destroy()

class Ventanados():
    def __init__(self,master,ven,u):
        #VENTANA 1
        self.ven = ven
        #NOMBRE USUARIO QUE INICIO SESION
        self.usuario = u
        #VENTANA 2
        self.dos = master

        self.dos.title('Programa 1')
        ancho = 500
        alto = 320
        ventana_ancho = self.dos.winfo_screenwidth()
        ventana_alto = self.dos.winfo_screenheight()
        x = (ventana_ancho // 2) - (ancho // 2)
        y = (ventana_alto // 2) - (alto // 2)
        self.dos.geometry(f'{ancho}x{alto}+{x}+{y}')

        Button(self.dos,text='Regresar',command=self.Regresar,width=10).place(x=150,y=140)

        self.us = Label(self.dos,text=f'Bienvenido \n {self.usuario}')
        self.us.place(x=400,y=1)
        
        self.Mostrar()
        self.mostrarTabla()
        #CREACION DEL MENU
        self.menus = tk.Menu(self.dos)
        self.dos.config(menu=self.menus)
        #SUBMENU "ARCHIVO"
        self.archivos = tk.Menu(self.menus,tearoff=0)
        self.archivos.add_command(label='Agregar',command=self.Crearusuario)
        self.indexAgregar = self.archivos.index("end")
        self.archivos.add_command(label='Modificar',command=self.Modificarus)
        self.indexModificar = self.archivos.index("end")
        self.archivos.add_command(label='Eliminar',command=self.Eliminarusr)
        self.indexEliminar = self.archivos.index("end")
        self.archivos.add_command(label='Salir',command=self.salir)
        self.menus.add_cascade(label='Archivo',menu=self.archivos)
        #INHABILITA LAS OPCIONES AGREGAR, MODIFICAR Y ELIMINAR
        self.archivos.entryconfig(self.indexAgregar,state = 'disable')
        self.archivos.entryconfig(self.indexEliminar,state = 'disable')
        self.archivos.entryconfig(self.indexModificar,state = 'disable')
        #ACTIVA OPCIONES DEPENDIENDO DEL USUARIO
        self.roles()

    def roles(self):
        #SI EL USUARIO ES admin PERMISO TOTAL, TODO EL MENU ACTIVADO
        if self.usuario == 'admin':
            self.archivos.entryconfig(self.indexAgregar,state='normal')
            self.archivos.entryconfig(self.indexEliminar,state='normal')
            self.archivos.entryconfig(self.indexModificar,state='normal')
        #SI EL USUARIO ES supervisor PUEDE AGREGAR SOLAMENTE
        elif self.usuario == 'Supervisor' or self.usuario == 'supervisor':
            self.archivos.entryconfig(self.indexAgregar,state='normal')
            self.archivos.entryconfig(self.indexEliminar,state='disable')
            self.archivos.entryconfig(self.indexModificar,state='disable')
        #SI EL USUARIO ES jefe de area PUEDE ELIMINAR SOLAMENTE
        elif self.usuario == 'Jefe de area' or self.usuario == 'jefe de area':
            self.archivos.entryconfig(self.indexAgregar,state='disable')
            self.archivos.entryconfig(self.indexEliminar,state='normal')
            self.archivos.entryconfig(self.indexModificar,state='disable')

    def Crearusuario(self):
        #VERIFICA CAJAS NO VACIAS
        if len(self.usu.get()) != 0 and len(self.pas.get()) != 0:
            #CONECTA A LA BASE DE DATOS
            con = sqlite3.connect("Usuarios.db")
            cursor = con.cursor()
            #INSERTA LOS DATOS A LA TABLA (USUARIO Y CONTRASEÑA)
            cursor.execute("INSERT INTO usuarios (usuario,password) VALUES (?,?)", (self.usu.get(), self.pas.get()))
            con.commit()
            con.close()
            self.Actualizartabla()
            self.borrarcaja('Usuario agregado correctamente')
        else:
            messagebox.showerror('Error','Faltan Datos')

    def Seleccionfila(self, event):
        #FILA SELECCIONADA
        try:
            index = self.tabla.selection()[0]
        except:
            return
        #OBTIENE LOS VALORES DE ESA FILA
        valores = self.tabla.item(index,"values")
        #LIMPIA CAJAS DE TEXTO
        self.usu.delete(0,END)
        self.pas.delete(0,END)
        #INSERTA LOS VALORES DEL REGSITRO SELECCIONADO
        self.usu.insert(0,valores[1])
        self.pas.insert(0,valores[2]) 
        
    def Actualizartabla(self):
        #LIMPIA TODA LA TABLA
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        #VUELVE A LLENAR LA TABLA
        self.mostrarTabla()

    def Modificarus(self):
        #VERIFICA QUE HAYA SELECCIONADO UN REGISTRO
        try:
            index = self.tabla.selection()[0]
        except:
            messagebox.showerror('Error','Elige un usuario')
            return
        #OBTIENE LOS VALORES DE ESA FILA
        valores = self.tabla.item(index,"values")
        id = valores[0]
        #CAJAS NO VACIAS
        if len(self.usu.get()) != 0 and len(self.pas.get()) != 0:
            #REALIZA LA MODIFICACION EN BASE DE DATOS
            u = self.usu.get()
            p = self.pas.get()
            #CONECTA A LA BASE DE DATOS
            con = sqlite3.connect("Usuarios.db")
            cursor = con.cursor()
            cursor.execute("UPDATE usuarios SET usuario=?, password=? WHERE id=?", (u, p, id))
            con.commit()
            con.close()
            self.Actualizartabla()
            self.borrarcaja('Usuario modificado correctamente')
        else:
            messagebox.showerror('Error','Faltan datos')

    def Eliminarusr(self):
        try:
            #OBTIENE LA FILA SELECCIONADA DE LA TABLA
            index = self.tabla.selection()[0]
            #EXTRAE LOS VALORES DE LA FILA
            valores = self.tabla.item(index,"values")
            #TOMA EL ID DEL USUARIO EN LA BASE DE DATOS
            id = int(valores[0])
            #NOMBRE DEL USUARIO
            usuario = valores[1]
            #BLOQUEA QUE EL USUARIO SE ELIMINE A SI MISMO
            if usuario == self.usuario:
                self.borrarcaja()
                messagebox.showerror('Error','No puedes eliminar tu propio usuario')
            else:
                #SI NO ES EL USUARIO ACTUAL, PROCEDE LA ELIMINACION
                con = sqlite3.connect("Usuarios.db")
                cursor = con.cursor()
                #ELIMINA EL USUARIO DE LA BASE 
                cursor.execute("DELETE FROM usuarios WHERE id=?", (id,))
                #REORGANIZA LOS ID PARA QUE NO QUEDEN HUECOS
                cursor.execute("UPDATE usuarios SET id = id - 1 WHERE id > ?", (id,))
                #REINICIA EL CONTADOR DE AUTOINCREMENT 
                cursor.execute("DELETE FROM sqlite_sequence WHERE name='usuarios'")
                con.commit()
                con.close()
                self.Actualizartabla()
                self.borrarcaja('Usuario borrado correctamente')
        except:
            messagebox.showerror('Error','Elige un usuario')
    
    #SALIR COMPLETAMENTE DE LAS DOS VENTANAS
    def salir(self):
        self.dos.destroy()
        self.ven.destroy()

    def mostrarTabla(self):
        con = sqlite3.connect("Usuarios.db")
        cursor = con.cursor()
        #SELECCIONA TODOS LOS REGISTROS 
        cursor.execute("SELECT * FROM usuarios")
        #INSERTA LOS DATOS EN EL TREEVIEW
        for i in cursor.fetchall():
            self.tabla.insert("",END,values=i)
        #CIERRA LA BASE DE DATOS
        con.close()

    def Mostrar(self):
        #CREA COLUMNAS PARA LA TABLA
        columnas = ("ID","USUARIO","PASSWORD")
        self.tabla = ttk.Treeview(self.dos,columns=columnas,show='headings')
        self.tabla.place(x=10,y=100,width=350,height=190)
        #POSICIONAR LA TABLA Y CONFIGURAR LAS COLUMNAS
        for col in columnas:
            self.tabla.heading(col,text=col)
            self.tabla.column(col,anchor='center',width=30)
        #CREA BARRAS DE DESPLAZAMIENTO
        scrolly = ttk.Scrollbar(self.dos,orient='vertical',command=self.tabla.yview)
        scrollx = ttk.Scrollbar(self.dos,orient='horizontal',command=self.tabla.xview)
        scrolly.place(x=360,y=90,height=200)
        scrollx.place(x=10,y=280,width=350)

        Label(self.dos,text='Escribe el usuario').place(x=10,y=10)
        self.usu = Entry(self.dos)
        self.usu.place(x=10,y=30)

        Label(self.dos,text='Escribe el password').place(x=150,y=10)
        self.pas = Entry(self.dos)
        self.pas.place(x=150,y=30)
        #VINCULAR UN EVENTO AL SELECCIONAR UNA FILA
        self.tabla.bind("<<TreeviewSelect>>",self.Seleccionfila)

    def borrarcaja(self,mensaje=''):
        self.usu.delete(0,END)
        self.pas.delete(0,END)
        if mensaje:
            messagebox.showinfo('Listo',mensaje)

    def Regresar(self):
        #CIERRA VENTANA 2
        self.dos.destroy()
        #MUESTRA NUEVAMENTE LA VENTANA 1
        self.ven.deiconify()

if __name__ == '__main__':
    crearBaseDatos()
    master = Tk()
    app = Ventana(master)
    app.Inicio()
    master.mainloop()
