"""
Bachelor in Data Science and Engineering 
Subject: Programming
Created by Camila Alba Agresta Kohen  
Created on 11/11/25 at 11:40
Universidad Carlos III de Madrid
Student

-------
Final project
Super Mario
"""
import constants
import pyxel
from character import Character

class Package:
    def __init__(self, x: int, y: int, dir: int, at_truck: bool, wait_frames: int = 2):
        """ This method creates the Character object
        :param x : the initial x of the character
        :param y : the initial y of the character
        """
        self.x = x
        self.y = y
        self.dir = dir
        #self.at_truck = at_truck
        self.wait_frames = wait_frames # para medir la velocidad del paquete
        self.sprite = constants.PACKAGE_SPRITE

        #self.check_collision_package()

        self.y_positions = constants.PACKAGE_Y_POSITIONS
        self.current_y_index = self.y_positions.index(y)

    # Creating properties and setters for the Character's attributes
    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @property
    def dir(self) -> int:
        return self.__dir

    @x.setter
    def x(self, x: int):
        if not isinstance(x, int):
            raise TypeError ("The x must be an integer " + str(type(x)) + "is provided")
        elif x < 0:
            raise ValueError("The x must be a non negative number")
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

    @dir.setter
    def dir(self, dir: int):
        if not isinstance(dir, int):
            raise TypeError(
                "The dir must be an integer " + str(type(dir)) + "is provided")
        elif dir < 0:
            raise ValueError("The dir must be a non negative number")
        else:
            self.__dir = dir

    def check_collision_package(self, character):
        # Definimos un tamaño para la colisión (ej. 12 px)
        size = 20

        if ((character.x < self.x + size) and
                (character.x + 12  > self.x) and  # 12 es el ancho aprox de Mario/Luigi
                (character.y < self.y + size) and
                (character.y + 16 > self.y)):  # 16 es el alto de Mario/Luigi
            return True
        else:
            return False

    def move_package(self, mario, luigi):
        """El paquete se mueve horizontalmente
        Se turna, en una cinta va de derecha a izquierda y en la siguiente de izquierda a derecha
        El paquete solo puede subir a la siguiente cinta si colisiona con luigi o mario"""
        # Verificamos que sea mayor que 0 para evitar el error de tu setter

        #print(self.current_y_index)
        #print(self.x)
        print(self.y)

        # y == 85 -> self.current_y_index == 4

        if pyxel.frame_count % self.wait_frames == 0:
            if self.current_y_index == 4:
                #if 84 <= self.x <= 265:
                if self.x > 0:
                    self.x -= 1 # se mueve hacia la izquierda

                #if self.check_collision_package(mario) or self.check_collision_package(luigi):
                    # AQUÍ PONES LO QUE PASA SI CHOCAN
                    #print("¡Colisión detectada! El paquete debería subir.")
                if self.check_collision_package(luigi):
                    self.y = 74
                    #self.y = self.y_positions.index(3)
                    self.current_y_index = 3

            if self.current_y_index == 3:
                if self.x > 0:
                    self.x += 1 # se mueve hacia la derecha
                if self.check_collision_package(mario):
                    self.y = 63
                    self.current_y_index = 2

            if self.current_y_index == 2:
                if self.x > 0:
                    self.x -= 1 # se mueve hacia la derecha
                if self.check_collision_package(luigi):
                    self.y = 52
                    self.current_y_index = 1

            if self.current_y_index == 1:
                if self.x > 0:
                    self.x += 1 # se mueve hacia la derecha
                if self.check_collision_package(mario):
                    self.y = 41
                    self.current_y_index = 0

            if self.current_y_index == 0:
                if self.x > 0:
                    self.x -= 1 # se mueve hacia la derecha
                if self.check_collision_package(luigi):
                    self.y = 41




