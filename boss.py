"""
Bachelor in Data Science and Engineering 
Subject: Programming
Created by Camila Alba Agresta Kohen  
Created on 21/11/25
Universidad Carlos III de Madrid
Student

-------
Final project

Clase Boss
El jefe que regaña a Mario y Luigi cuando se cae un paquete
"""
import constants

class Boss:
    def __init__(self, x: int, y: int):
        """ This method creates the Boss object
        :param x : the initial x of the boss
        :param y : the initial y of the boss
        """
        self.x = x
        self.y = y
        # De momento usa el sprite de Mario hasta que se cree el diseño del boss
        self.sprite = constants.BOSS_SPRITE
        self.is_visible = False  # El boss solo aparece cuando se cae un paquete

    # Creating properties and setters for the Boss's attributes
    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @property
    def is_visible(self) -> bool:
        return self.__is_visible

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

    @is_visible.setter
    def is_visible(self, visible: bool):
        if not isinstance(visible, bool):
            raise TypeError("The is_visible must be a boolean")
        else:
            self.__is_visible = visible

    def show(self):
        """Muestra al boss en pantalla"""
        self.is_visible = True

    def hide(self):
        """Oculta al boss de la pantalla"""
        self.is_visible = False
