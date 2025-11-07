"""
Bachelor in Data Science and Engineering 
Subject: Programming
Created by Camila Alba Agresta Kohen  
Created on 30/9/25 at 23:27
Universidad Carlos III de Madrid
Student

-------
Final Project: Super Mario Bros
Board V02
"""

import pyxel
import constants
#from mario_V01 import Mario
from character import Character
from mario_V02 import Mario

class Board:
    """This class contains a simple board"""

    def __init__(self, width: int, height: int):
        """ Method that creates the board.
        :param width: The width of the board
        :param height: The height of the board
        """
        # Setting the attributes
        self.width = width
        self.height = height

        # Start coordinates of the elements
        self.mario = Mario(constants.MARIO_START[0], constants.MARIO_START[1])

        # Initialization pyxel
        pyxel.init(self.width, self.height, title = "Mario Bros")
        # Loading the pyxres file with the images
        # AGREGAR CARPETAS DIFERENTES DENTRO DE ASSATS PARA PERSONAJES - FONDO - LABERINTO
        pyxel.load("assets/characters.pyxres")

        # Running the game
        pyxel.run(self.update, self.draw)

    def update(self):
        """Executed every frame: input & logic."""
        # To exit the game
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # Horizontal movement (solo Mario)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.mario.move('right', self.width)
        if pyxel.btn(pyxel.KEY_LEFT):
            self.mario.move('left', self.width)

    def draw(self):
        """Executed every frame: render."""
        # Erasing the previous screen
        pyxel.cls(0)
        # Drawing Mario (x, y, *sprite)
        pyxel.blt(self.mario.x, self.mario.y, *self.mario.sprite)
