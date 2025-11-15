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

class Package:
    def __init__(self, x: int, y: int, dir: int, at_truck: bool):
        """ This method creates the Character object
        :param x : the initial x of the character
        :param y : the initial y of the character
        """
        self.x = x
        self.y = y
        self.dir = dir
        #self.at_truck = at_truck
        # 2. Asigna el sprite como un ATRIBUTO
        #    La tupla es (banco_img, x_en_banco, y_en_banco, ancho, alto)
        self.sprite = constants.PACKAGE_SPRITE

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

    def move_package(self, board_x_size: int, board_y_size: int):
        if self.dir == 0:
            if (self.x  < board_x_size):
                self.x += 1
            else:
                self.dir = 1
        elif self.dir == 1:
            if (self.y  < board_y_size):
                self.y += 1
            else:
                self.dir = 2
        elif self.dir == 2:
            if (self.x > 0):
                self.x -= 1
            else:
                self.dir = 3
        elif self.dir == 3:
            if (self.y > 0):
                self.y -= 1
            else:
                self.dir = 0
