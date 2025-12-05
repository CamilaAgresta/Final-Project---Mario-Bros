"""
Conveyor Class
Represents a conveyor belt segment.
"""

import constants

class Conveyor:
    """Represents a conveyor belt."""

    def __init__(self, x: int, y: int):
        """
        Initializes the Conveyor object.
        :param x: The initial x coordinate of the conveyor
        :param y: The initial y coordinate of the conveyor
        """
        self.x = x
        self.y = y

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @x.setter
    def x(self, x: int):
        if not isinstance(x, int):
            raise TypeError(f"The x must be an integer, {type(x)} provided")
        elif x < 0:
            raise ValueError("The x must be a non-negative number")
        else:
            self.__x = x

    @y.setter
    def y(self, y: int):
        if not isinstance(y, int):
            raise TypeError(f"The y must be an integer, {type(y)} provided")
        elif y < 0:
            raise ValueError("The y must be a non-negative number")
        else:
            self.__y = y

