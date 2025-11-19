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
from background import Background
from mario_V02 import Mario
from character import Character
from mario_V02 import Mario
from luigi_V01 import Luigi
from package_V02 import Package
from truck import Truck


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
        self.luigi = Luigi(constants.LUIGI_START[0], constants.LUIGI_START[1])
        self.background = Background(constants.BACKGROUND_START[0], constants.BACKGROUND_START[1])
        self.package = Package(constants.PACKAGE_START[0], constants.PACKAGE_START[1], 0, False, wait_frames = 4)
        self.truck = Truck(constants.TRUCK_START[0], constants.TRUCK_START[1],0,False)

        # Initialization pyxel
        pyxel.init(self.width, self.height, title = "Mario Bros")
        # Loading the pyxres file with the images
        # AGREGAR CARPETAS DIFERENTES DENTRO DE ASSATS PARA PERSONAJES - FONDO - LABERINTO
        pyxel.load("assets/characters.pyxres")
        #pyxel.load("assets/fondo.pyxres")

        # Running the game
        pyxel.run(self.update, self.draw)

    def update(self):
        """Executed every frame: input & logic."""
        # To exit the game
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # --- Controles de Mario (Flechas) ---
        if pyxel.btnp(pyxel.KEY_UP):
            self.mario.move_vertical('up')
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.mario.move_vertical('down')

        # --- Controles de Luigi (W y S) ---
        if pyxel.btnp(pyxel.KEY_W):
            self.luigi.move_vertical('up')
        if pyxel.btnp(pyxel.KEY_S):
            self.luigi.move_vertical('down')

        # --- MOVIMIENTO AUTOMÁTICO DEL PAQUETE ---
        #self.package.move_package()

        # --- Presentación de Mario y luigi a la clase paquete ---
        self.package.move_package(self.mario, self.luigi)

        self.package.check_collision_package(self.mario, self.luigi)


    def draw(self):
        """Executed every frame: render."""
        # Erasing the previous screen
        pyxel.cls(0)
        # Dibuja el fondo PRIMERO (desde Banco 1)
        pyxel.blt(self.background.x, self.background.y, *self.background.sprite)
        # Drawing Mario (x, y, *sprite)
        pyxel.blt(self.mario.x, self.mario.y, *self.mario.sprite)
        # Drawing Luigi (x, y, *sprite)
        pyxel.blt(self.luigi.x, self.luigi.y, *self.luigi.sprite)
        # Drawing Package (x, y, *sprite)
        pyxel.blt(self.package.x, self.package.y, *self.package.sprite)
        # Drawing Truck (x, y, *sprite)
        pyxel.blt(self.truck.x, self.truck.y, *self.truck.sprite)

