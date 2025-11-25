"""
Bachelor in Data Science and Engineering 
Subject: Programming
Created by Camila Alba Agresta Kohen  
Created on 11/11/25 at 12:33
Universidad Carlos III de Madrid
Student

-------
Final project

Clase camión
"""
import constants

class Truck:
    def __init__(self, x: int, y: int, dir: int, truck_full: bool):
        """ This method creates the Character object
        :param x : the initial x of the character
        :param y : the initial y of the character
        """
        self.x = x
        self.y = y
        #self.dir = dir
        #self.truck_full = truck_full
        self.sprite = constants.TRUCK_SPRITE
        self.packages_count = 0  # Contador de paquetes en el camión (empezar con 7 para pruebas)
        self.is_leaving = False  # Si el camión está yendo
        self.initial_x = x  # Guardar posición inicial

    # Creating properties and setters for the Character's attributes
    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    #@property
    #def dir(self) -> int:
        #return self.__dir

    #@property
    #def truck_full(self) -> bool:
        #return self.__truck_full

    @x.setter
    def x(self, x: int):
        if not isinstance(x, int):
            raise TypeError ("The x must be an integer " + str(type(x)) + "is provided")
        # Permitir valores negativos para que el camión pueda salir de pantalla
        else:
            self.__x = x

    @y.setter
    def y(self, y: int):
        if not isinstance(y, int):
            raise TypeError ("The y must be an integer " + str(type(y)) + "is provided")
        elif y < 0:
            raise ValueError("The y must be a non negative number")
        else:
            self.__y = y

    #@dir.setter
    #def dir(self, dir: int):
        #if not isinstance(dir, int):
            #raise TypeError(
                #"The dir must be an integer " + str(type(dir)) + "is provided")
        #elif dir < 0:
            #raise ValueError("The dir must be a non negative number")
        #else:
            #self.__dir = dir

    #@truck_full.setter
    #def truck_full(self,full:bool):
        #pass

    def add_package(self):
        """Añade un paquete al camión"""
        self.packages_count += 1
        print(f"Paquete añadido al camión. Total: {self.packages_count}/8")
        if self.packages_count >= 8:
            self.is_leaving = True
            print("¡Camión lleno! Se va...")

    def update(self):
        """Actualiza el estado del camión"""
        if self.is_leaving:
            self.x -= 2  # El camión se mueve hacia la izquierda
            # Si el camión sale de la pantalla, reiniciarlo
            if self.x < -30:
                self.x = self.initial_x
                self.packages_count = 0
                self.is_leaving = False
                print("Nuevo camión listo para recibir paquetes")

    def is_full(self):
        """Verifica si el camión está lleno"""
        return self.packages_count >= 8
