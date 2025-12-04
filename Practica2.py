#LIBRERIAS/LIBRARIES
from tkinter import * 
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import sqlite3

#CREACION BASE DE DATOS/DATABASE CREATION
def crearBaseDatos():
    #CONECTAR BASE DE DATOS LLAMDA Usuarios.db
    #CONNECT TO DATABASE NAMED Usuarios.db
    con = sqlite3.connect("Usuarios.db")
    cursor = con.cursor()
    #CREA LA TABLA 
    #CREATE THE TABLE
    cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL,password TEXT NOT NULL)""")
    #VERIFICA SI EXISTE EL USUARIO "admin"
    #CHECK IF USER "admin" EXISTS
    cursor.execute("SELECT * FROM usuarios WHERE usuario='admin'")
    #FETOCHE DEVUELVE REGISTRO NONE, SI NO EXISTE ENTRA AL IF
    #FETCHONE RETURNS NONE IF NO RECORD EXISTS, THEN ENTER IF
    if not cursor.fetchone():
        #INSERTA USUARIO POR DEFECTO/INSERT DEFAULT USER
        cursor.execute("INSERT INTO usuarios (usuario,password) VALUES (?,?)",("admin","12345"))
    #GUARDA CAMBIOS Y CERRAR/SAVE CHANGES AND CLOSE
    con.commit()
    con.close()

#CLASE VENTANA 1/WINDOW 1 CLASS
class Ventana():
    #TAMAÑO DE VENTANA/WINDOW SIZE
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
    
    #INTERFAZ VENTANA 1/WINDOW 1 INTERFACE
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
        #GET DATA FROM TEXTBOXES
        u = self.n1.get()
        p = self.n2.get()
        #CONECTA CON LA BASE DE DATOS/CONNECT TO DATABASE
        con = sqlite3.connect("Usuarios.db")
        cursor = con.cursor()
        #VERIFICA SI EXISTE EL USUARIO/CHECK IF USER EXISTS
        cursor.execute("SELECT * FROM usuarios WHERE usuario=? and password=?", (u,p))
        #OBTIENE EL RESULTADO/GET RESULT
        resultado = cursor.fetchone()
        #CIERRA LA CONEXION/CLOSE DATABASE CONNECTION
        con.close()
        #SI EL RESULTADO SE ENCUENTRA ENTONCES..
        #IF RESULT FOUND THEN...
        if resultado:
            #LIMPIA CAJAS DE TEXTO/CLEAR TEXTBOXES
            self.n1.delete(0,END)
            self.n2.delete(0,END)
            #OCULTA LA VENTANA 1/HIDE WINDOW 1
            self.ven.withdraw()
            #CREA VENTANA 2/CREATE WINDOW 2
            otra = Toplevel(self.ven)
            #ABRE LA VENTANA 2/OPEN WINDOW 2
            Ventanados(otra,self.ven,u)
        else:
            messagebox.showerror('Error','Datos incorrectos')
            self.n1.delete(0,END)
            self.n2.delete(0,END)
            
    #CIERRA TOTALMENTE LAS VENTANAS CON BOTON SALIR
    #COMPLETELY CLOSE WINDOWS WITH EXIT BUTTON
    def Cerrar(self):
        self.ven.destroy()

#CLASE VENTANA 2/WINDOW 2 CLASS
class Ventanados():
    #TAMAÑO VENTANA 2/WINDOW 2 SIZE
    def __init__(self,master,ven,u):
        #VENTANA 1/WINDOW 1
        self.ven = ven
        #NOMBRE USUARIO QUE INICIO SESION
        #USERNAME THAT LOGGED IN
        self.usuario = u
        #VENTANA 2/WINDOW 2
        self.dos = master
        
        #TAMAÑO DE VENTANA 2/WINDOW 2 SIZE
        self.dos.title('Programa 1')
        ancho = 500
        alto = 320
        ventana_ancho = self.dos.winfo_screenwidth()
        ventana_alto = self.dos.winfo_screenheight()
        x = (ventana_ancho // 2) - (ancho // 2)
        y = (ventana_alto // 2) - (alto // 2)
        self.dos.geometry(f'{ancho}x{alto}+{x}+{y}')
        
        #INTERFAZ DE VENTANA 2/WINDOW 2 INTERFACE
        Button(self.dos,text='Regresar',command=self.Regresar,width=10).place(x=150,y=140)

        self.us = Label(self.dos,text=f'Bienvenido \n {self.usuario}')
        self.us.place(x=400,y=1)
        
        self.Mostrar()
        self.mostrarTabla()
        #CREACION DEL MENU/MENU CREATION
        self.menus = tk.Menu(self.dos)
        self.dos.config(menu=self.menus)
        #SUBMENU "ARCHIVO"/SUBMENU "ARCHIVO"
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
        #DISABLE ADD, MODIFY AND DELETE OPTIONS
        self.archivos.entryconfig(self.indexAgregar,state = 'disable')
        self.archivos.entryconfig(self.indexEliminar,state = 'disable')
        self.archivos.entryconfig(self.indexModificar,state = 'disable')
        #ACTIVA OPCIONES DEPENDIENDO DEL USUARIO
        #ENABLE OPTIONS DEPENDING ON USER
        self.roles()

    def roles(self):
        #SI EL USUARIO ES admin PERMISO TOTAL, TODO EL MENU ACTIVADO
        #IF USER IS admin, FULL PERMISSION, ALL MENU ENABLED
        if self.usuario == 'admin':
            self.archivos.entryconfig(self.indexAgregar,state='normal')
            self.archivos.entryconfig(self.indexEliminar,state='normal')
            self.archivos.entryconfig(self.indexModificar,state='normal')
        #SI EL USUARIO ES supervisor PUEDE AGREGAR SOLAMENTE
        #IF USER IS supervisor CAN ONLY ADD
        elif self.usuario == 'Supervisor' or self.usuario == 'supervisor':
            self.archivos.entryconfig(self.indexAgregar,state='normal')
            self.archivos.entryconfig(self.indexEliminar,state='disable')
            self.archivos.entryconfig(self.indexModificar,state='disable')
        #SI EL USUARIO ES jefe de area PUEDE ELIMINAR SOLAMENTE
        #IF USER IS jefe de area CAN ONLY DELETE
        elif self.usuario == 'Jefe de area' or self.usuario == 'jefe de area':
            self.archivos.entryconfig(self.indexAgregar,state='disable')
            self.archivos.entryconfig(self.indexEliminar,state='normal')
            self.archivos.entryconfig(self.indexModificar,state='disable')

    def Crearusuario(self):
        #VERIFICA CAJAS NO VACIAS/CHECK NON-EMPTY TEXTBOXES
        if len(self.usu.get()) != 0 and len(self.pas.get()) != 0:
            #CONECTA A LA BASE DE DATOS/CONNECT TO DATABASE
            con = sqlite3.connect("Usuarios.db")
            cursor = con.cursor()
            #INSERTA LOS DATOS A LA TABLA (USUARIO Y CONTRASEÑA)
            #INSERT DATA INTO TABLE (USER AND PASSWORD)
            cursor.execute("INSERT INTO usuarios (usuario,password) VALUES (?,?)", (self.usu.get(), self.pas.get()))
            con.commit()
            con.close()
            self.Actualizartabla()
            self.borrarcaja('Usuario agregado correctamente')
        else:
            messagebox.showerror('Error','Faltan Datos')

    def Seleccionfila(self, event):
        #FILA SELECCIONADA/#ELECTED ROW
        try:
            index = self.tabla.selection()[0]
        except:
            return
        #OBTIENE LOS VALORES DE ESA FILA
        #GET VALUES FROM THAT ROW
        valores = self.tabla.item(index,"values")
        #LIMPIA CAJAS DE TEXTO/CLEAR TEXTBOXES
        self.usu.delete(0,END)
        self.pas.delete(0,END)
        #INSERTA LOS VALORES DEL REGSITRO SELECCIONADO
        #INSERT SELECTED RECORD VALUES
        self.usu.insert(0,valores[1])
        self.pas.insert(0,valores[2]) 
        
    def Actualizartabla(self):
        #LIMPIA TODA LA TABLA/CLEAR ENTIRE TABLE
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        #VUELVE A LLENAR LA TABLA/REFILL TABLE
        self.mostrarTabla()

    def Modificarus(self):
        #VERIFICA QUE HAYA SELECCIONADO UN REGISTRO
        #CHECK IF A RECORD IS SELECTED
        try:
            index = self.tabla.selection()[0]
        except:
            messagebox.showerror('Error','Elige un usuario')
            return
        #OBTIENE LOS VALORES DE ESA FILA
        #GET VALUES FROM THAT ROW
        valores = self.tabla.item(index,"values")
        id = valores[0]
        #CAJAS NO VACIAS/TEXTBOXES NOT EMPTY
        if len(self.usu.get()) != 0 and len(self.pas.get()) != 0:
            #REALIZA LA MODIFICACION EN BASE DE DATOS
            #UPDATE RECORD IN DATABASE
            u = self.usu.get()
            p = self.pas.get()
            #CONECTA A LA BASE DE DATOS/CONNECT TO DATABASE
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
            #GET SELECTED ROW
            index = self.tabla.selection()[0]
            #EXTRAE LOS VALORES DE LA FILA/EXTRACT VALUES FROM ROW
            valores = self.tabla.item(index,"values")
            #TOMA EL ID DEL USUARIO EN LA BASE DE DATOS
            #GET ID OF USER IN DATABASE
            id = int(valores[0])
            #NOMBRE DEL USUARIO/USERNAME
            usuario = valores[1]
            #BLOQUEA QUE EL USUARIO SE ELIMINE A SI MISMO
            #PREVENT USER FROM DELETING THEMSELVES
            if usuario == self.usuario:
                self.borrarcaja()
                messagebox.showerror('Error','No puedes eliminar tu propio usuario')
            else:
                #SI NO ES EL USUARIO ACTUAL, PROCEDE LA ELIMINACION
                #IF NOT CURRENT USER, PROCEED TO DELETE
                con = sqlite3.connect("Usuarios.db")
                cursor = con.cursor()
                #ELIMINA EL USUARIO DE LA BASE 
                #DELETE USER FROM DATABASE
                cursor.execute("DELETE FROM usuarios WHERE id=?", (id,))
                #REORGANIZA LOS ID PARA QUE NO QUEDEN HUECOS
                #REORGANIZE IDS SO THERE ARE NO GAPS
                cursor.execute("UPDATE usuarios SET id = id - 1 WHERE id > ?", (id,))
                #REINICIA EL CONTADOR DE AUTOINCREMENT 
                #RESET AUTOINCREMENT COUNTER
                cursor.execute("DELETE FROM sqlite_sequence WHERE name='usuarios'")
                con.commit()
                con.close()
                self.Actualizartabla()
                self.borrarcaja('Usuario borrado correctamente')
        except:
            messagebox.showerror('Error','Elige un usuario')
    
    #SALIR COMPLETAMENTE DE LAS DOS VENTANAS
    #EXIT COMPLETELY FROM BOTH WINDOWS
    def salir(self):
        self.dos.destroy()
        self.ven.destroy()

    def mostrarTabla(self):
        con = sqlite3.connect("Usuarios.db")
        cursor = con.cursor()
        #SELECCIONA TODOS LOS REGISTROS 
        #SELECT ALL RECORDS
        cursor.execute("SELECT * FROM usuarios")
        #INSERTA LOS DATOS EN EL TREEVIEW
        #INSERT DATA INTO TREEVIEW
        for i in cursor.fetchall():
            self.tabla.insert("",END,values=i)
        #CIERRA LA BASE DE DATOS
        #CLOSE DATABASE
        con.close()

    def Mostrar(self):
        #CREA COLUMNAS PARA LA TABLA
        #CREATE COLUMNS FOR TABLE
        columnas = ("ID","USUARIO","PASSWORD")
        self.tabla = ttk.Treeview(self.dos,columns=columnas,show='headings')
        self.tabla.place(x=10,y=100,width=350,height=190)
        #POSICIONAR LA TABLA Y CONFIGURAR LAS COLUMNAS
        #POSITION THE TABLE AND CONFIGURE COLUMNS
        for col in columnas:
            self.tabla.heading(col,text=col)
            self.tabla.column(col,anchor='center',width=30)
        #CREA BARRAS DE DESPLAZAMIENTO/CREATE SCROLLBARS
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
        #CIERRA VENTANA 2/CLOSE WINDOW 2
        self.dos.destroy()
        #MUESTRA NUEVAMENTE LA VENTANA 1/SHOW WINDOW 1 AGAIN
        self.ven.deiconify()

if __name__ == '__main__':
    crearBaseDatos()
    master = Tk()
    app = Ventana(master)
    app.Inicio()
    master.mainloop()
