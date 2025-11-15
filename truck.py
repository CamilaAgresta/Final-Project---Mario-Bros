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
