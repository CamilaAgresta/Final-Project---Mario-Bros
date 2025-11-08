"""
Bachelor in Data Science and Engineering 
Subject: Programming
Created by Camila Alba Agresta Kohen  
Created on 8/11/25 at 21:13
Universidad Carlos III de Madrid
Student

-------

Subclass Luigi
"""

from character import Character
import constants

class Luigi(Character):
    def __init__(self, x: int, y: int):
        """
        Metodo constructor para Mario.
        Llama al constructor de la clase padre (Character) y
        asigna el sprite específico de Mario.
        """
        # 1. Llama al __init__ de la clase padre (Character)
        #    para inicializar self.x y self.y
        super().__init__(x, y)

        # 2. Asigna el sprite como un ATRIBUTO
        #    La tupla es (banco_img, x_en_banco, y_en_banco, ancho, alto)
        self.sprite = constants.LUIGI_SPRITE

        # 3. Guarda las posiciones Y permitidas
        self.y_positions = constants.LUIGI_Y_POSITIONS
        # 4. Guarda el índice de la posición Y actual
        #    (Como MARIO_START es (215, 83), y 83 es el último en la tupla,
        #    el índice inicial será 2)
        try:
            self.current_y_index = self.y_positions.index(y)
        except ValueError:
            # Si la Y inicial no está en la lista, se asigna la primera
            self.current_y_index = 0
            self.y = self.y_positions[0]

    def move_vertical(self, direction: str):
        """Mueve a Mario verticalmente entre las posiciones Y predefinidas."""

        if direction.lower() == 'up':
            # Mueve a una Y más pequeña (más arriba en la pantalla)
            # Si el índice actual es > 0, puede subir
            if self.current_y_index > 0:
                self.current_y_index -= 1
                self.y = self.y_positions[self.current_y_index]

        elif direction.lower() == 'down':
            # Mueve a una Y más grande (más abajo en la pantalla)
            # Si el índice actual es menor que el último índice (longitud - 1), puede bajar
            if self.current_y_index < len(self.y_positions) - 1:
                self.current_y_index += 1
                self.y = self.y_positions[self.current_y_index]
