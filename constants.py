"""
Bachelor in Data Science and Engineering 
Subject: Programming
Created by Camila Alba Agresta Kohen  
Created on 30/9/25 at 22:35
Universidad Carlos III de Madrid
Student

-------
Final Project: Super Mario Bros
Constants
"""
# significado tupla XXX_SPRITE
# La tupla es (banco_img, x_en_banco, y_en_banco, ancho, alto)

# ---------------------------------
# Dimension of the screen
WIDTH = 288
HIGH = 118

# ---------------------------------
# Fondo
BACKGROUND_START = (16,16)
BACKGROUND_SPRITE = (1, 0, 0, 256, 100)

# ---------------------------------
# MARIO
MARIO_START = (215, 83)
MARIO_SPRITE = (0, 0, 0, 12, 16) #12 de ancho x 16 de alto, Mario ocupa el primer cuadrante

# Posiciones Y permitidas para Mario (de arriba a abajo: 39, 61, 83)
MARIO_Y_POSITIONS = (39, 61, 83)

# ---------------------------------
# LUIGI
LUIGI_START = (60, 72)
LUIGI_SPRITE = (0, 0, 16, 12, 16)
LUIGI_Y_POSITIONS = (28, 50, 72)

# ---------------------------------
# PACKAGE
PACKAGE_START = (265,85)
PACKAGE_SPRITE = (0, 0, 32, 4, 3)

# ---------------------------------
# TRUCK (18 alto x 22 ancho aprox)
TRUCK_START = (24,52)
TRUCK_SPRITE = (0, 0, 40, 22, 18)