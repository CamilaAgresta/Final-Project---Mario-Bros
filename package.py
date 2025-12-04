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
    def __init__(self, x: int, y: int, dir: int, at_truck: bool, wait_frames: int = 2, difficulty: str = "EASY", conveyor_speeds: dict = None):
        """ This method creates the Character object
        :param x : the initial x of the character
        :param y : the initial y of the character
        """
        self.x = x
        self.y = y
        self.dir = dir
        #self.at_truck = at_truck
        self.wait_frames = constants.PACKAGE_WAIT_FRAMES # para medir la velocidad del paquete
        self.difficulty = difficulty
        self.conveyor_speeds = conveyor_speeds if conveyor_speeds else {}
        self.move_accumulator = 0.0 # Acumulador para movimiento fraccionario (Crazy mode)
        self.sprite = constants.PACKAGE_SPRITE_1  # Empieza con el primer sprite

        self.is_falling = False # Variable para saber si está cayendo
        self.fall_start_frame = None # Frame en el que empezó a caer
        self.fall_frame_counter = 0  # Contador para ralentizar la caída

        self.y_positions = constants.PACKAGE_Y_POSITIONS
        # --- PRUEBA DE LA VERDAD ---
        print("LA LISTA REAL ES:", self.y_positions)

        self.current_y_index = self.y_positions.index(y)
        
        # Ajustar velocidad si es dificultad MEDIA y está en cinta impar (1, 3, 5)
        # Cintas impares: indices 0 (cinta 5), 2 (cinta 3), 4 (cinta 1 - parte izq)
        # Nota: Cinta 1 comparte index 4 con Cinta 0. Se ajustará dinámicamente en move_package
        if self.difficulty == "MEDIUM":
             # Velocidad base más rápida para cintas impares (wait_frames menor = más rápido)
             # Si wait_frames es 2, 1.5x velocidad sería wait_frames = 1.33 (redondeado a 1)
             pass 
        
        # Contador de veces que ha pasado por zona invisible
        self.invisible_count = 0
        self.was_invisible = False  # Para detectar cuando sale de zona invisible

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

    def package_visible(self):
        """Determina si el paquete es visible y cambia el sprite al salir de zona invisible"""
        # Ya no necesitamos devolver True/False para dibujar, porque draw() se encarga
        # Pero mantenemos la lógica de cambio de sprite
        
        # Zona invisible definida en constants
        start_invisible = constants.INVISIBLE_ZONE_X[0]
        end_invisible = constants.INVISIBLE_ZONE_X[1]
        
        # Está completamente dentro de la zona invisible?
        is_fully_invisible = (self.x > start_invisible and self.x + self.sprite[3] < end_invisible)
        
        # Detectar cuando entra en zona TOTALMENTE invisible
        # Si antes NO estaba totalmente invisible y ahora SI lo está, cambiamos el sprite
        # Usamos un atributo nuevo 'was_fully_invisible' para detectar el flanco de subida
        if not hasattr(self, 'was_fully_invisible'):
            self.was_fully_invisible = False

        if not self.was_fully_invisible and is_fully_invisible:
            # Acaba de entrar completamente en la zona invisible
            self.invisible_count += 1
            print(f"¡Paquete totalmente oculto! Contador: {self.invisible_count}")
            
            # Cambiar sprite AHORA, para que cuando salga ya tenga el nuevo
            if self.invisible_count == 1:
                self.sprite = constants.PACKAGE_SPRITE_2
                print("→ Cambiado a SPRITE 2 (listo para salir)")
            elif self.invisible_count >= 2:
                self.sprite = constants.PACKAGE_SPRITE_3
                print("→ Cambiado a SPRITE 3 (listo para salir)")
        
        # Actualizar estado para la próxima vez
        self.was_fully_invisible = is_fully_invisible
        
        return not is_fully_invisible

    def draw(self):
        """Dibuja el paquete con recorte (clipping) si está entrando/saliendo de la zona invisible"""
        img = self.sprite[0]
        u = self.sprite[1]
        v = self.sprite[2]
        w = self.sprite[3]
        h = self.sprite[4]
        
        start_invisible = constants.INVISIBLE_ZONE_X[0]
        end_invisible = constants.INVISIBLE_ZONE_X[1]
        
        # Caso 1: Totalmente visible (fuera de la zona y sus bordes)
        if self.x + w <= start_invisible or self.x >= end_invisible:
            pyxel.blt(self.x, self.y, img, u, v, w, h)
            
        # Caso 2: Entrando a la zona invisible (se recorta la derecha)
        elif self.x < start_invisible < self.x + w:
            # Ancho visible es la distancia hasta el inicio de la zona invisible
            visible_w = start_invisible - self.x
            pyxel.blt(self.x, self.y, img, u, v, visible_w, h)
            
        # Caso 3: Saliendo de la zona invisible (se recorta la izquierda)
        elif self.x < end_invisible < self.x + w:
            # Cuánto se ha salido ya (ancho visible)
            visible_w = (self.x + w) - end_invisible
            # Offset en X para dibujar (empieza en end_invisible)
            draw_x = end_invisible
            # Offset en la textura (saltamos la parte que sigue oculta)
            skip_w = w - visible_w
            pyxel.blt(draw_x, self.y, img, u + skip_w, v, visible_w, h)
            
        # Caso 4: Totalmente dentro (no se dibuja nada)
        else:
            pass

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
        
        # Si ha pasado más de 0.5 segundos cayendo, lanzar error
        if time_falling > 0.5:
            raise RuntimeError(f"¡PAQUETE PERDIDO! El paquete cayó sin ser atrapado en la posición x={self.x}, y={self.y}")
        
        # Caer más lento: solo actualizar Y cada 2 frames (mitad de velocidad)
        self.fall_frame_counter += 1
        if self.fall_frame_counter >= 2:
            self.y += 1  # Velocidad de caída más lenta
            self.fall_frame_counter = 0

    def check_collision_package(self, mario, luigi):
        # PAQUETE SOBRE CINTA
        # 85 = constants.CONVEYOR_Y[0]
        # CONVEYOR 0 - solo parte derecha (antes de Mario) en y=85
        if (self.y == constants.CONVEYOR_Y[0] and constants.CONVEYOR_0_X < self.x):
            return "package in conveyor"
        # CONVEYOR 1 - solo parte izquierda (después de Mario) en y=85
        elif (self.y == constants.CONVEYOR_Y[0] and constants.CONVEYOR_ODD_X[0] <= self.x <= constants.CONVEYOR_ODD_X[1]):
            return "package in conveyor"
        # Resto de cintas
        elif (((self.y == constants.CONVEYOR_Y[1] or self.y == constants.CONVEYOR_Y[3]) and constants.CONVEYOR_EVEN_X[0] <= self.x <= constants.CONVEYOR_EVEN_X[1]) or
              ((self.y == constants.CONVEYOR_Y[2] or self.y == constants.CONVEYOR_Y[4]) and constants.CONVEYOR_ODD_X[0] <= self.x <= constants.CONVEYOR_ODD_X[1])):
            return "package in conveyor"

        # MARIO - detecta cuando el paquete sale por el lado derecho de las cintas
        elif ((mario.y == constants.MARIO_Y_POSITIONS[2] and constants.CONVEYOR_ODD_X[1] <= self.x <= constants.CONVEYOR_0_X and abs(self.y - constants.CONVEYOR_Y[0]) <= 8) or  # CONVEYOR 0 -> CONVEYOR 1
                (mario.y == constants.MARIO_Y_POSITIONS[1] and self.x >= constants.CONVEYOR_EVEN_X[1] and abs(self.y - constants.CONVEYOR_Y[1]) <= 8) or
                (mario.y == constants.MARIO_Y_POSITIONS[0] and self.x >= constants.CONVEYOR_EVEN_X[1] and abs(self.y - constants.CONVEYOR_Y[3]) <= 8)):
            return "collision mario"
        # LUIGI - detecta cuando el paquete sale por el lado izquierdo de las cintas
        elif ((luigi.y == constants.LUIGI_Y_POSITIONS[2] and self.x <= constants.CONVEYOR_ODD_X[0] and abs(self.y - constants.CONVEYOR_Y[0]) <= 8) or  # CONVEYOR 1 -> siguiente cinta (y=74)
                (luigi.y == constants.LUIGI_Y_POSITIONS[1] and self.x <= constants.CONVEYOR_ODD_X[0] and abs(self.y - constants.CONVEYOR_Y[2]) <= 8) or
                (luigi.y == constants.LUIGI_Y_POSITIONS[0] and self.x <= constants.CONVEYOR_ODD_X[0] and abs(self.y - constants.CONVEYOR_Y[4]) <= 8)):
            return "collision luigi"
        else:
            #self.fall()
            return "no collision"

    def move_package(self, mario, luigi):
        """El paquete se mueve horizontalmente
        Se turna, en una cinta va de derecha a izquierda y en la siguiente de izquierda a derecha
        El paquete solo puede subir a la siguiente cinta si colisiona con luigi o mario"""

        # Lógica de velocidad según dificultad
        # EASY: Todas las cintas 1x (cada 2 frames)
        # MEDIUM: Impares 1.5x (2 de cada 3 frames), resto 1x
        # EXTREME: Conv0=1x, Pares=1.5x, Impares=2x (cada frame)
        
        # Identificar tipo de cinta
        is_conveyor_0 = False
        is_odd_conveyor = False
        is_even_conveyor = False
        
        # Conveyor 0: parte derecha del index 4 (x > CONVEYOR_0_X)
        if self.current_y_index == 4 and self.x > constants.CONVEYOR_0_X:
            is_conveyor_0 = True
        # Cintas impares: 5 (index 0), 3 (index 2), 1 (index 4 izquierda)
        elif self.current_y_index in [0, 2]:
            is_odd_conveyor = True
        elif self.current_y_index == 4 and constants.CONVEYOR_ODD_X[0] <= self.x <= constants.CONVEYOR_ODD_X[1]:
            is_odd_conveyor = True
        # Cintas pares: 4 (index 1), 2 (index 3)
        elif self.current_y_index in [1, 3]:
            is_even_conveyor = True
        
        # Aplicar velocidad según dificultad y tipo de cinta
        # Aplicar velocidad según dificultad y tipo de cinta
        if self.difficulty == "CRAZY":
            multiplier = 1.0
            
            if is_conveyor_0:
                multiplier = 1.0
            else:
                # Obtener multiplicador del diccionario (usando current_y_index)
                # Nota: para index 4 izquierda, usamos key 4
                multiplier = self.conveyor_speeds.get(self.current_y_index, 1.0)
            
            # Velocidad base es 0.5 px/frame (1 cada 2 frames)
            speed = 0.5 * multiplier
            self.move_accumulator += speed
            
            if self.move_accumulator >= 1.0:
                self.move_accumulator -= 1.0
                # Continuar para mover
            else:
                return # No mover en este frame
                
        elif self.difficulty == "EXTREME":
            if is_odd_conveyor:
                # Impares en EXTREME: 2x velocidad (cada frame)
                pass  # Siempre se mueve
            elif is_even_conveyor:
                # Pares en EXTREME: 1.5x velocidad (2 de cada 3 frames)
                if pyxel.frame_count % 3 != 0:
                    pass  # Continuar
                else:
                    return  # Saltar este frame
            else:  # is_conveyor_0
                # Conveyor 0 en EXTREME: 1x velocidad normal
                if pyxel.frame_count % self.wait_frames != 0:
                    return
        elif self.difficulty == "MEDIUM":
            if is_odd_conveyor:
                # Impares en MEDIUM: 1.5x velocidad (2 de cada 3 frames)
                if pyxel.frame_count % 3 != 0:
                    pass  # Continuar
                else:
                    return  # Saltar este frame
            else:
                # Resto en MEDIUM: 1x velocidad normal
                if pyxel.frame_count % self.wait_frames != 0:
                    return
        else:  # EASY
            # EASY: todas las cintas 1x velocidad normal
            if pyxel.frame_count % self.wait_frames != 0:
                return

        # y == 85 -> self.current_y_index == 4

        # Guardamos el estado para no llamar a la función varias veces y hacer el código más limpio
        collision_status = self.check_collision_package(mario, luigi)

        # --- CONVEYOR 0 (Parte derecha - donde aparece el paquete, y=85) ---
        # Usamos un flag especial para distinguir CONVEYOR 0 de CONVEYOR 1
        # Ambos tienen current_y_index=4 pero diferentes rangos X
        if self.current_y_index == 4 and self.x > constants.CONVEYOR_ODD_X[1]:
            if collision_status == "package in conveyor":
                self.is_falling = False  # Resetear estado de caída
                self.fall_start_frame = None
                self.x -= 1  # se mueve hacia la izquierda
            elif collision_status == "collision mario":
                print("collision with Mario at point x=", self.x," y=",self.y)
                self.is_falling = False  # Resetear estado de caída
                self.fall_start_frame = None
                self.fall_start_frame = None
                # NO cambia Y, solo X (pasa de parte derecha a parte izquierda)
                self.x = constants.CONVEYOR_ODD_X[1]  # Comienza en el lado derecho de CONVEYOR 1
                self.y = constants.CONVEYOR_Y[0] # Asegurar que Y se resetea si lo atrapamos cayendo
                return True  # Retorna True porque el paquete pasó a la siguiente cinta
            else:
                self.fall()

        # --- CONVEYOR 1 (Parte izquierda - misma altura y=85, pero x <= 204) ---
        elif self.current_y_index == 4 and self.x <= constants.CONVEYOR_ODD_X[1]:
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
                self.x = constants.CONVEYOR_EVEN_X[0]
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
                self.x = constants.CONVEYOR_ODD_X[1]
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
                self.x = constants.CONVEYOR_EVEN_X[0]
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
