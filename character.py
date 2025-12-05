"""
Final project

Character Class
Base class for Mario and Luigi
"""

import constants

class Character:
    """
    This class represents a generic character for the final project.
    This character only moves horizontally (conceptually, though subclasses move vertically).
    """

    def __init__(self, x: int, y: int):
        """
        Creates the Character object.
        :param x: The initial x coordinate of the character
        :param y: The initial y coordinate of the character
        """
        self.x = x
        self.y = y

    # Properties and setters for the Character's attributes
    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @x.setter
    def x(self, x: int):
        if not isinstance(x, int):
            raise TypeError("The x must be an integer, " + str(type(x)) + " provided")
        elif x < 0:
            raise ValueError("The x must be a non-negative number")
        else:
            self.__x = x

    @y.setter
    def y(self, y: int):
        if not isinstance(y, int):
            raise TypeError("The y must be an integer, " + str(type(y)) + " provided")
        elif y < 0:
            raise ValueError("The y must be a non-negative number")
        else:
            self.__y = y





