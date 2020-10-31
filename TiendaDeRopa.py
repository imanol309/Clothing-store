from os import system


class Usuarios:
    
    def login(self):
        name = input("Incresa tu nombre de usuario:")
        contra = input("Incresa tu contraseña de usuario:")
        
        nombre = "yordi"
        contraseña = "852518"
        
        if name == nombre and contra == contraseña:
            system("cls")
            print("bien")
        else:
            
            system("cls")
            print('Esa no es tu cuenta correcta')
            Usuarios1.login()

Usuarios1 = Usuarios()
Usuarios1.login()
