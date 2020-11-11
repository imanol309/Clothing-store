from tkinter import ttk
from tkinter import *

import sqlite3

class Productos:

    db_name = 'base1.db'
    
    def __init__(self,ventana):
        
        # Creador de la ventalla de programa
        self.wind = ventana
        self.wind.title("Productos de ventas")

        #Contenedor
        frame = LabelFrame(self.wind, text = 'Registrar nuevos productos')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 10)


        #Nombre de producto
        Label(frame, text = 'name: ').grid(row = 1, column = 0)
        self.Nombre = Entry(frame)
        self.Nombre.focus()
        self.Nombre.grid(row = 1, column = 1)

        #Precio de producto
        Label(frame, text = 'price: ').grid(row = 2, column = 0)
        self.Precio = Entry(frame)
        self.Precio.grid(row = 2, column = 1)

        #cantidad de productos
        Label(frame, text = 'cantidad: ').grid(row = 3, column = 0)
        self.Cantidad = Entry(frame)
        self.Cantidad.grid(row = 3, column = 1)
    
        #Boton para agregar productos
        ttk.Button(frame, text = 'Agregar Productos', command = self.Agregar_productos).grid(row = 5, columnspan = 2, sticky = W + E)


        #Aviso de datos
        self.aviso = Label(text = '', fg = 'red')
        self.aviso.grid(row = 4, column = 0, columnspan = 2, sticky = W + E)

        #Tabla de datos
        self.tabla = ttk.Treeview(height = 15)
        self.tabla['columns'] = ('one', 'two')
        self.tabla.grid(row = 5, column = 0, columnspan = 2)
        self.tabla.heading('#0', text = 'name', anchor = CENTER)
        self.tabla.heading('#1', text = 'price', anchor = CENTER)
        self.tabla.heading('#2', text = 'cantidad', anchor = CENTER)
        
        #boton de eliminar productos
        ttk.Button(text = 'Eliminar', command = self.eleminar_productos).grid(row = 6, columnspan = 2, sticky = W)
        
        
        #boton de editar productos
        ttk.Button(text = 'Editar', command = self.editar_pruductos).grid(row = 6, columnspan = 2, sticky = E)
        
        
        self.get_Productos() 
        
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor() 
            result = cursor.execute(query, parameters)
            conn.commit()
        return result
    
    def get_Productos(self):
        # #limpiar tabla
        records = self.tabla.get_children()
        for element in records:
            self.tabla.delete(element)

        #quering datos
        query = 'SELECT * FROM product ORDER BY name DESC'
        db_rows = self.run_query(query)
        print(db_rows)
        
        for row in db_rows:
            self.tabla.insert('', 0, text = row[1], values = row[2])
        
    # Validacion de los productos ingresados       
    def validacion(self):
        return len(self.Nombre.get()) != 0 and len(self.Precio.get()) != 0 and len(self.Cantidad.get()) != 0 
    
    # visualizacion de los productos. 
    def Agregar_productos(self):
        if self.validacion():
            query = 'INSERT INTO product VALUES(NULL, ?, ?, ?)'
            parameters = (self.Nombre.get(), self.Precio.get(), self.Cantidad.get())
            self.run_query(query, parameters)
            self.aviso['text'] = 'El producto {} asi agregado'.format(self.Nombre.get())
            self.Nombre.delete(0, END)
            self.Precio.delete(0, END)
            self.Cantidad.delete(0, END)
        else:
            self.aviso['text'] = 'El producto es necesarios agregar'
        self.get_Productos()
        
    # funcion para eliminar los productos no deseados
    def eleminar_productos(self):
        self.aviso['text'] = ''
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.aviso['text'] = 'POR FAVOR SELECIONA UN PRODUCTO'  
            return
        self.aviso['text'] = ''
        name = self.tabla.item(self.tabla.selection())['text']
        query =  'DELETE FROM product WHERE name = ?'
        self.run_query(query, (name, ))
        self.aviso['text'] = 'El producto {} asi eliminado'.format(name)
        self.get_Productos()
    
    #Editar productos 
    def editar_pruductos(self):
        
        self.aviso['text'] = ''
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.aviso['text'] = 'POR FAVOR SELECIONA UN PRODUCTO'  
            return
        name = self.tabla.item(self.tabla.selection())['text']
        price = self.tabla.item(self.tabla.selection())['values'][0]
        
        # Nueva ventana para editar los productos
        self.ventana_segunda = Toplevel()
        self.ventana_segunda.title = 'Ventana de editar productos'
        
        
        # viejo nombre
        Label(self.ventana_segunda, text = 'Viejo nombre: ').grid(row = 0, column = 1)
        Entry(self.ventana_segunda, textvariable = StringVar(self.ventana_segunda, value = name), state = 'readonly').grid(row = 0, column = 2)
        
        
        # nuevo nombre
        Label(self.ventana_segunda, text = 'Nuevo Nombre: ').grid(row = 1, column = 1)
        new_name = Entry(self.ventana_segunda)
        new_name.grid(row = 1, column = 2)
        
        
        # viejo precio
        Label(self.ventana_segunda, text = 'Viejo Precio: ').grid(row = 2, column = 1)
        Entry(self.ventana_segunda, textvariable = StringVar(self.ventana_segunda, value = price), state = 'readonly').grid(row = 2, column = 2)
        
        # Nuevo Precio
        Label(self.ventana_segunda, text = 'Nuevo Precio: ').grid(row = 3, column = 1)
        new_precio= Entry(self.ventana_segunda)
        new_precio.grid(row = 3, column = 2)
        
        
        #Boton de editar nuevo
        Button(self.ventana_segunda, text = 'Cambiar', command = lambda: self.Editar(new_name.get(), name, new_precio.get(),price)).grid(row = 4, column = 2, sticky = W + E)
        
    
    def Editar(self, new_name, name, new_precio, price):
        query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
        parameters = (new_name, new_precio, name, price)
        self.run_query(query, parameters)
        self.ventana_segunda.destroy()
        self.aviso['text'] = 'Producto {} editado'.format(name)
        self.get_Productos()
        
        
if __name__ == '__main__':
    ventana = Tk()
    aplicacion = Productos(ventana)
    ventana.mainloop()