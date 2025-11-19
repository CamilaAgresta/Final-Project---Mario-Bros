"""
Bachelor in Data Science and Engineering 
Subject: Programming
Created by Camila Alba Agresta Kohen  
Created on 19/11/25 at 18:56
Universidad Carlos III de Madrid
Student

-------
Lab x
Exercise: xxx
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

        #self.is_falling = False # Variable para saber si está cayendo

        self.y_positions = constants.PACKAGE_Y_POSITIONS
        # --- PRUEBA DE LA VERDAD ---
        print("LA LISTA REAL ES:", self.y_positions)

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
    def fall(self):
        """El metodo fall sirve para determinar que pasa cuando se cae un paquete (no hay colisión)
        Va asociado a perder una vida y a que el jefe regañe a mario y luigi"""
        self.y += 2  # Velocidad de caída (puedes cambiarla)

    def check_collision_package(self, mario, luigi):
        # PAQUETE SOBRE CINTA
        if ((self.y == 85 and 83 <= self.x <= 204 or 229 < self.x) or
                ((self.y == 74 or self.y == 52) and 80 <= self.x <= 201) or
                ((self.y == 63 or self.y == 41) and 83 <= self.x <= 204)):
            return "package in conveyor"

        # MARIO
        elif ((mario.y == 83 and 204 <= self.x <= 229 and self.y == 85) or
                (mario.y == 61 and self.x >= 201 and self.y == 74) or
                #(mario.y == 61 and self.x > 204 and self.y == 63) or
                (mario.y == 39 and self.x >= 201 and self.y == 52)):
                #(mario.y == 39 and self.x > 204 and self.y == 41) or
            return "collision mario"
        elif ((luigi.y == 72 and self.x <= 83 and self.y == 85) or
                (luigi.y == 50 and self.x <= 83 and self.y == 63) or
                (luigi.y == 28 and self.x <= 83 and self.y == 41)):
            return "collision luigi"
        else:
            #self.fall()
            return "no collision"

    def move_package(self, mario, luigi):
        """El paquete se mueve horizontalmente
        Se turna, en una cinta va de derecha a izquierda y en la siguiente de izquierda a derecha
        El paquete solo puede subir a la siguiente cinta si colisiona con luigi o mario"""

        print("actual position x=",self.x," y=",self.y)

        if pyxel.frame_count % self.wait_frames != 0:
            return

        # y == 85 -> self.current_y_index == 4

        # Guardamos el estado para no llamar a la función varias veces y hacer el código más limpio
        collision_status = self.check_collision_package(mario, luigi)

        # --- CONVEYOR 1 (Abajo del todo) ---
        if self.current_y_index == 4:
            if collision_status == "package in conveyor" or collision_status == "collision mario":
                self.x -= 1  # se mueve hacia la izquierda
            elif collision_status == "collision luigi":
                print("collision with Luigi at point x=", self.x," y=",self.y)
                self.y = self.y_positions[self.current_y_index-1]
                self.current_y_index -= 1
                self.x = 83
                return
            else:
                self.fall()

        # --- CONVEYOR 2 and 4  ---
        if self.current_y_index == 3 or self.current_y_index == 1:
            if collision_status == "package in conveyor":
                self.x += 1  # se mueve hacia la derecha
            elif collision_status == "collision mario":
                print("collision with Mario at point x=", self.x, " y=", self.y)
                self.y = self.y_positions[self.current_y_index-1]
                self.current_y_index -= 1
                self.x = 204
                return
            else:
                self.fall()

        # --- CONVEYOR 3  ---
        if self.current_y_index == 2:
            if collision_status == "package in conveyor":
                self.x -= 1  # se mueve hacia la izquierda
            elif collision_status == "collision luigi":
                print("collision with Luigi at point x=", self.x, " y=", self.y)
                self.y = self.y_positions[self.current_y_index-1]
                self.current_y_index -= 1
                self.x = 83
                return
            else:
                self.fall()

        # --- CONVEYOR 5 (last one)  ---
        if self.current_y_index == 0:
            if collision_status == "package in conveyor" or collision_status == "collision luigi":
                self.x -= 1  # se mueve hacia la izquierda
            else:
                self.fall()
