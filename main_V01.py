"""
Bachelor in Data Science and Engineering 
Subject: Programming
Created by Camila Alba Agresta Kohen  
Created on 30/9/25 at 22:23
Universidad Carlos III de Madrid
Student

-------
Final Project: Super Mario Bros
Main code V01
"""
#hola

### COMANDOS PARA IR SUBIENDO A GITHUB
## Ejecutar en la terminal

# git remote -v

# git pull origin main  (traer los cambios más recientes desde GitHub a tu carpeta local)

# git add .
# git commit -m "mensaje corto explicando el cambio"

# git push origin main

####################################
# Ejecutar cada vez que quiera modificar el/los dibujos
# pyxel edit assets/xxxx (general)
# personajes -> pyxel edit assets/characters.pyxres

# pyxel edit assets/fondo

####################################

import constants
from board_V02 import Board

# Creating the board object will also initialize pyxel
board = Board(constants.WIDTH, constants.HIGH)