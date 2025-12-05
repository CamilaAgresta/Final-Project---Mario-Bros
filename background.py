"""
Background Class
Game background management
"""

import constants

class Background:
    """Represents the game background."""

    def __init__(self, x: int, y: int):
        """
        Initializes the Background object.
        :param x: The initial x coordinate of the background
        :param y: The initial y coordinate of the background
        """
        self.x = x
        self.y = y
        self.sprite = constants.BACKGROUND_SPRITE

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

