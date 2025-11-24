"""
Bachelor in Data Science and Engineering 
Subject: Programming
Created by Camila Alba Agresta Kohen  
Created on 19/11/25 at 18:56
Universidad Carlos III de Madrid
Student

-------
Lab x
Exercise: xxx
"""

import constants
import pyxel
from character import Character

class Package:
    def __init__(self, x: int, y: int, dir: int, at_truck: bool, wait_frames: int = 2):
        """ This method creates the Character object
        :param x : the initial x of the character
        :param y : the initial y of the character
        """
        self.x = x
        self.y = y
        self.dir = dir
        #self.at_truck = at_truck
        self.wait_frames = constants.PACKAGE_WAIT_FRAMES # para medir la velocidad del paquete
        self.sprite = constants.PACKAGE_SPRITE

        self.is_falling = False # Variable para saber si está cayendo
        self.fall_start_frame = None # Frame en el que empezó a caer
        self.fall_frame_counter = 0  # Contador para ralentizar la caída

        self.y_positions = constants.PACKAGE_Y_POSITIONS
        # --- PRUEBA DE LA VERDAD ---
        print("LA LISTA REAL ES:", self.y_positions)

        self.current_y_index = self.y_positions.index(y)

    # Creating properties and setters for the Character's attributes
    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @property
    def dir(self) -> int:
        return self.__dir

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

    @dir.setter
    def dir(self, dir: int):
        if not isinstance(dir, int):
            raise TypeError(
                "The dir must be an integer " + str(type(dir)) + "is provided")
        elif dir < 0:
            raise ValueError("The dir must be a non negative number")
        else:
            self.__dir = dir
    def fall(self):
        """El metodo fall sirve para determinar que pasa cuando se cae un paquete (no hay colisión)
        Va asociado a perder una vida y a que el jefe regañe a mario y luigi"""
        # Si es la primera vez que cae, guardar el frame actual
        if not self.is_falling:
            self.is_falling = True
            self.fall_start_frame = pyxel.frame_count
            self.fall_frame_counter = 0
        
        # Calcular el tiempo transcurrido desde que empezó a caer (en segundos)
        # pyxel corre a 30 fps por defecto
        frames_falling = pyxel.frame_count - self.fall_start_frame
        time_falling = frames_falling / 30.0  # convertir frames a segundos
        
        # Si ha pasado más de 0.3 segundos cayendo, lanzar error
        if time_falling > 0.3:
            raise RuntimeError(f"¡PAQUETE PERDIDO! El paquete cayó sin ser atrapado en la posición x={self.x}, y={self.y}")
        
        # Caer más lento: solo actualizar Y cada 2 frames (mitad de velocidad)
        self.fall_frame_counter += 1
        if self.fall_frame_counter >= 2:
            self.y += 1  # Velocidad de caída más lenta
            self.fall_frame_counter = 0

    def check_collision_package(self, mario, luigi):
        # PAQUETE SOBRE CINTA
        # CONVEYOR 0 - solo parte derecha (antes de Mario) en y=85
        if (self.y == 85 and 229 < self.x):
            return "package in conveyor"
        # CONVEYOR 1 - solo parte izquierda (después de Mario) en y=85
        elif (self.y == 85 and 83 <= self.x <= 204):
            return "package in conveyor"
        # Resto de cintas
        elif (((self.y == 74 or self.y == 52) and 80 <= self.x <= 201) or
              ((self.y == 63 or self.y == 41) and 83 <= self.x <= 204)):
            return "package in conveyor"

        # MARIO - detecta cuando el paquete sale por el lado derecho de las cintas
        elif ((mario.y == 83 and 204 <= self.x <= 229 and self.y == 85) or  # CONVEYOR 0 -> CONVEYOR 1
                (mario.y == 61 and self.x >= 201 and self.y == 74) or
                (mario.y == 61 and self.x >= 204 and self.y == 63) or
                (mario.y == 39 and self.x >= 201 and self.y == 52) or
                (mario.y == 39 and self.x >= 204 and self.y == 41)):
            return "collision mario"
        # LUIGI - detecta cuando el paquete sale por el lado izquierdo de las cintas
        elif ((luigi.y == 72 and self.x <= 83 and self.y == 85) or  # CONVEYOR 1 -> siguiente cinta (y=74)
                (luigi.y == 50 and self.x <= 83 and self.y == 63) or
                (luigi.y == 28 and self.x <= 83 and self.y == 41)):
            return "collision luigi"
        else:
            #self.fall()
            return "no collision"

    def move_package(self, mario, luigi):
        """El paquete se mueve horizontalmente
        Se turna, en una cinta va de derecha a izquierda y en la siguiente de izquierda a derecha
        El paquete solo puede subir a la siguiente cinta si colisiona con luigi o mario"""

        if pyxel.frame_count % self.wait_frames != 0:
            return

        # y == 85 -> self.current_y_index == 4

        # Guardamos el estado para no llamar a la función varias veces y hacer el código más limpio
        collision_status = self.check_collision_package(mario, luigi)

        # --- CONVEYOR 0 (Parte derecha - donde aparece el paquete, y=85) ---
        # Usamos un flag especial para distinguir CONVEYOR 0 de CONVEYOR 1
        # Ambos tienen current_y_index=4 pero diferentes rangos X
        if self.current_y_index == 4 and self.x > 204:
            if collision_status == "package in conveyor":
                self.is_falling = False  # Resetear estado de caída
                self.fall_start_frame = None
                self.x -= 1  # se mueve hacia la izquierda
            elif collision_status == "collision mario":
                print("collision with Mario at point x=", self.x," y=",self.y)
                self.is_falling = False  # Resetear estado de caída
                self.fall_start_frame = None
                # NO cambia Y, solo X (pasa de parte derecha a parte izquierda)
                self.x = 204  # Comienza en el lado derecho de CONVEYOR 1
                return True  # Retorna True porque el paquete pasó a la siguiente cinta
            else:
                self.fall()

        # --- CONVEYOR 1 (Parte izquierda - misma altura y=85, pero x <= 204) ---
        elif self.current_y_index == 4 and self.x <= 204:
            if collision_status == "package in conveyor":
                self.is_falling = False  # Resetear estado de caída
                self.fall_start_frame = None
                self.x -= 1  # se mueve hacia la izquierda
            elif collision_status == "collision luigi":
                print("collision with Luigi at point x=", self.x," y=",self.y)
                self.is_falling = False  # Resetear estado de caída
                self.fall_start_frame = None
                # AHORA SÍ cambia de Y (sube a la cinta de arriba)
                self.y = self.y_positions[self.current_y_index-1]  # Pasa a y=74
                self.current_y_index -= 1
                self.x = 83
                return True  # Retorna True porque el paquete pasó a la siguiente cinta
            else:
                self.fall()

        # --- CONVEYOR 2 and 4  ---
        elif self.current_y_index == 3 or self.current_y_index == 1:
            if collision_status == "package in conveyor":
                self.is_falling = False  # Resetear estado de caída
                self.fall_start_frame = None
                self.x += 1  # se mueve hacia la derecha
            elif collision_status == "collision mario":
                print("collision with Mario at point x=", self.x, " y=", self.y)
                self.is_falling = False  # Resetear estado de caída
                self.fall_start_frame = None
                self.y = self.y_positions[self.current_y_index-1]
                self.current_y_index -= 1
                self.x = 204
                return True  # Retorna True porque el paquete pasó a la siguiente cinta
            else:
                self.fall()

        # --- CONVEYOR 3  ---
        elif self.current_y_index == 2:
            if collision_status == "package in conveyor":
                self.is_falling = False  # Resetear estado de caída
                self.fall_start_frame = None
                self.x -= 1  # se mueve hacia la izquierda
            elif collision_status == "collision luigi":
                print("collision with Luigi at point x=", self.x, " y=", self.y)
                self.is_falling = False  # Resetear estado de caída
                self.fall_start_frame = None
                self.y = self.y_positions[self.current_y_index-1]
                self.current_y_index -= 1
                self.x = 83
                return True  # Retorna True porque el paquete pasó a la siguiente cinta
            else:
                self.fall()

        # --- CONVEYOR 5 (last one)  ---
        elif self.current_y_index == 0:
            if collision_status == "package in conveyor":
                self.is_falling = False  # Resetear estado de caída
                self.fall_start_frame = None
                self.x -= 1  # se mueve hacia la izquierda
            elif collision_status == "collision luigi":
                print("Luigi envió el paquete al camión!")
                return "to_truck"  # Señal especial para enviar al camión
            else:
                self.fall()
        
        return False  # No hubo paso de paquete a siguiente cinta
