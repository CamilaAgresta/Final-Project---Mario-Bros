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
DISPLAY_SCALE = 4

# ---------------------------------
# Fondo
BACKGROUND_START = (16,16)
BACKGROUND_SPRITE = (1, 0, 0, 256, 100)
INVISIBLE_ZONE_X = (125, 162)

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
CONVEYOR_0_X = 229
CONVEYOR_ODD_X = (83, 204)
CONVEYOR_EVEN_X = (80, 201)

CONVEYOR_Y = (83, 72, 61, 50, 39)

# ---------------------------------
# PACKAGE
PACKAGE_START = (265, 83)  # Empieza en CONVEYOR 0 (parte derecha, 2 píxeles más arriba)

# Sprites del paquete (cambian al pasar por zonas invisibles)
PACKAGE_SPRITE_1 = (0, 27, 6, 11, 5)   # Sprite inicial
PACKAGE_SPRITE_2 = (0, 27, 14, 11, 5)  # Sprite después de 1ra vez invisible
PACKAGE_SPRITE_3 = (0, 29, 22, 7, 5)  # Sprite después de 2da vez invisible

# Sprite por defecto (para compatibilidad)
PACKAGE_SPRITE = PACKAGE_SPRITE_1

# Posiciones Y de las cintas transportadoras
# IMPORTANTE: CINTA 0 y CINTA 1 comparten la misma Y (85) pero diferentes rangos X
PACKAGE_Y_POSITIONS = (39, 50, 61, 72, 83)  # 5 alturas diferentes (2 píxeles más arriba)
PACKAGE_WAIT_FRAMES = 2 # cuanto más grande va más lento

# coordenadas Y paquete sobre cinta transportadora
# cinta0 = 83 (index 4) - parte DERECHA (x > 229)
# cinta1 = 83 (index 4) - parte IZQUIERDA (83 <= x <= 204) 
# cinta2 = 72 (index 3)
# cinta3 = 61 (index 2)
# cinta4 = 50 (index 1)
# cinta5 = 39 (index 0)

# coordenadas X segun cinta transportadora
# cinta 0 -> x > 229 (parte derecha, antes de Mario)
# cinta 1 -> 83 <= x <= 204 (parte izquierda, después de Mario)
# cinta 2 y 4 -> 80 < X < 201
# cinta 3 y 5 -> 83 < X < 204

# POSITIONS PACKAGES AT TRUCK (camión quieto)
# paquete 1 -> x = 36, y = 60
# paquete 2 -> x = 41, y = 60

#PACKAGE_TRUCK_X = (36,41)
#PACKAGE_TRUCK_Y = (60,56,52,48)

TRUCK_PACKAGE_POSITIONS = [
    (36, 58), # Paquete 1 (índice 0) - 2 píxeles más arriba
    (41, 58), # Paquete 2 (índice 1) - 2 píxeles más arriba
    (36, 54), # Paquete 3 (índice 2) - 2 píxeles más arriba
    (41, 54), # Paquete 4 (índice 3) - 2 píxeles más arriba
    (36, 50), # Paquete 5 (índice 4) - 2 píxeles más arriba
    (41, 50), # Paquete 6 (índice 5) - 2 píxeles más arriba
    (36, 46), # Paquete 7 (índice 6) - 2 píxeles más arriba
    (41, 46)  # Paquete 8 (índice 7) - 2 píxeles más arriba
]

# ---------------------------------
# TRUCK (18 alto x 24 ancho - extendido 2 píxeles a la derecha)
TRUCK_START = (24,52)
TRUCK_SPRITE = (0, 0, 40, 24, 18)

# ---------------------------------
# BOSS
MARIO_FAIL = (249, 60)
LUIGI_FAIL = (26, 83)
BOSS_SPRITE_1 = (0, 0, 64, 12, 16)  # De momento usa el sprite de Mario
BOSS_SPRITE_2 = (0, 16, 64, 18, 16)  # De momento usa el sprite de Mario

# ---------------------------------
# LIVE
LIVE_SPRITE = (0, 0, 0, 12, 7)
