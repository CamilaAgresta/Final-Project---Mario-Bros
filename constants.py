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
# Posiciones Y permitidas para Luigi (de arriba a abajo: 28, 50, 72)
LUIGI_Y_POSITIONS = (28, 50, 72)

# ---------------------------------
# CONVEYOR
CONVEYOR_1_X = (83, 265, 204, 229)

# ---------------------------------
# PACKAGE
PACKAGE_START = (265, 96)  # Ahora empieza en la cinta más baja (CONVEYOR 0)
PACKAGE_SPRITE = (0, 0, 32, 4, 3)

# Posiciones Y de las cintas transportadoras (de arriba a abajo : 41, 52, 63, 74, 85, 96)
PACKAGE_Y_POSITIONS = (41, 52, 63, 74, 85, 96)

# coordenadas Y paquete sobre cinta transportadora
# cinta0 = 96 (5) - NUEVA: Cinta inicial donde aparece el paquete
# cinta1 = 85 (4)
# cinta2 = 74 (3)
# cinta3 = 63 (2)
# cinta4 = 52 (1)
# cinta5 = 41 (0)

# coordenadas X segun cinta transportadora
# cinta 0 -> 83 < X < 265 , agujero entre 204 < X < 229 (Mario atrapa aquí)
# cinta 1 -> 83 < X < 265 , agujero entre 204 < X < 229
# cinta 2 y 4 -> 80 < X < 201
# cinta 3 y 5 -> 83 < X < 204

# ---------------------------------
# TRUCK (18 alto x 22 ancho aprox)
TRUCK_START = (24,52)
TRUCK_SPRITE = (0, 0, 40, 22, 18)

# ---------------------------------
# BOSS
BOSS_START = (140, 20)
BOSS_SPRITE = (0, 0, 0, 12, 16)  # De momento usa el sprite de Mario