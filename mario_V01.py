"""
Bachelor in Data Science and Engineering 
Subject: Programming
Created by Camila Alba Agresta Kohen  
Created on 30/9/25 at 22:41
Universidad Carlos III de Madrid
Student

-------
Final Project: Super Mario Bros
Mario V01
"""

import constants

class Mario:
    """This class is simple example of how to represent a character for the final project.
    This character only moves horizontally."""

    def __init__(self, x: int, y: int):
        """ This method creates the Character object
        :param x : the initial x of the character
        :param y : the initial y of the character
        """
        self.x = x
        self.y = y
        # The sprite will be always the same, so no parameter is needed
        # The tuple is (image_bank, starting_x, starting_y, horizontal_size, vertical_size)
        # It would be a good idea to make the sprite read-only, we will see how to do it in lectures
        self.sprite = constants.MARIO_SPRITE

    # Creating properties and setters for the Character's attributes
    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

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

    def move(self, direction: str, board_x_size: int):
        """ This is an example of how to move the character horizontally. No obstacles in the board
        are considered.
        :param direction: a string which can be left or right
        :param board_x_size: the horizontal size of the board, to check the limits
        """
        # Local variable to store the width of the character to check collisions with right border
        # of the board
        x_size = self.sprite[3]
        if (direction.lower() == "right" and self.x + x_size < board_x_size):
            self.x += 1
        elif (direction.lower() == "left" and self.x > 0):
            self.x -= 1
