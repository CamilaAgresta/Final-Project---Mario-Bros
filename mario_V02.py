"""
Bachelor in Data Science and Engineering 
Subject: Programming
Created by Camila Alba Agresta Kohen  
Created on 7/11/25 at 18:50
Universidad Carlos III de Madrid
Student

-------
Mario
subclase de Character
"""
from character import Character
import constants

class Mario(Character):
    def __init__(self, x: int, y: int):
        """
        Método constructor para Mario.
        Llama al constructor de la clase padre (Character) y
        asigna el sprite específico de Mario.
        """
        # 1. Llama al __init__ de la clase padre (Character)
        #    para inicializar self.x y self.y
        super().__init__(x, y)

        # 2. Asigna el sprite como un ATRIBUTO
        #    La tupla es (banco_img, x_en_banco, y_en_banco, ancho, alto)
        self.sprite = constants.MARIO_SPRITE

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

