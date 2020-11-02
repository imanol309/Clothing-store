from os import system
from tkinter import ttk
from tkinter import *

import sqlite3

class Productos:

    db_name = 'Base.db'
    
    def __init__(self,ventana):
        
        # Creador de la ventalla de programa
        self.wind = ventana
        self.wind.title("Productos de ventas")

        #Contenedor
        frame = LabelFrame(self.wind, text = 'Registrar nuevos productos')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 10)


        #Nombre de producto
        Label(frame, text = ' name: ').grid(row = 1, column = 0)
        self.Nombre = Entry(frame)
        self.Nombre.focus()
        self.Nombre.grid(row = 1, column = 1)


        #Precio de producto
        Label(frame, text = 'price: ').grid(row = 2, column = 0)
        self.Precio = Entry(frame)
        self.Precio.grid(row = 2, column = 1)


        #Boton para agregar productos
        ttk.Button(frame, text = 'Agregar Productos', command = self.Agregar_productos).grid(row = 3, columnspan = 2, sticky = W + E)


        #Tabla de datos
        self.tabla = ttk.Treeview(height = 10, column = 3)
        self.tabla.grid(row = 4, column = 0, columnspan = 3)
        self.tabla.heading('#0', text = 'name', anchor = CENTER)
        self.tabla.heading('#1', text = 'price', anchor = CENTER)
        
        
        
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
        return len(self.Nombre.get()) != 0 and len(self.Precio.get()) != 0
    
    # visualizacion de los productos.
    def Agregar_productos(self):
        if self.validacion():
            print(self.Nombre.get())
            print(self.Precio.get())
        else:
            print('Nombre y Precio es obligado')
            

if __name__ == '__main__':
    ventana = Tk()
    aplicacion = Productos(ventana)
    ventana.mainloop()