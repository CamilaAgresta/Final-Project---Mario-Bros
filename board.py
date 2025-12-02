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
from character import Character
from mario import Mario
from luigi import Luigi
from package import Package
from truck import Truck
from boss import Boss


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
        self.package = Package(constants.PACKAGE_START[0], constants.PACKAGE_START[1], 0, False, wait_frames = 1) # Hay que borrarla despues
        self.truck = Truck(constants.TRUCK_START[0], constants.TRUCK_START[1],0,False)
        self.boss = Boss(constants.MARIO_FAIL[0], constants.MARIO_FAIL[1])

        # Sistema de vidas
        self.lives = 3
        self.boss_display_frames = 0  # Contador para mostrar al boss temporalmente
        self.score = 0  # Puntuación del juego
        self.break_time = 0  # Contador para el descanso cuando el camión se llena
        self.is_frozen = False # Estado de congelación del juego
        self.freeze_timer = 0 # Temporizador para la congelación
        
        # Game state management
        self.game_state = "MENU"  # Puede ser: "MENU", "PLAYING", "GAME_OVER"
        self.menu_selection = 0  # 0 = Play, 1 = Quit
        self.difficulty_selection = 0  # 0 = Easy, 1 = Medium
        self.difficulty = "EASY"  # Se establece al empezar el juego
        self.deliveries_count = 0  # Contador de entregas exitosas (para recuperación de vida en Medium)

        # System of packages
        self.packages = []

        # Variables para controlar la aparición (spawn) de paquetes
        self.pending_spawns = 0  # Cuántos paquetes quedan por salir en esta tanda
        self.spawn_timer = 0  # Temporizador para el retraso entre paquetes
        # NO iniciamos paquetes aquí, se inician cuando se selecciona Play en el menú




        # Initialization pyxel
        pyxel.init(self.width, self.height, title = "Mario Bros", display_scale=constants.DISPLAY_SCALE)
        # Loading the pyxres file with the images
        # AGREGAR CARPETAS DIFERENTES DENTRO DE ASSATS PARA PERSONAJES - FONDO - LABERINTO
        pyxel.load("assets/characters.pyxres")
        #pyxel.load("assets/fondo.pyxres")

        # Running the game
        pyxel.run(self.update, self.draw)

    def schedule_new_packages(self):
        """Calcula cuántos paquetes lanzar según la puntuación"""

        # 1. Calculamos cuántos grupos llevamos según dificultad
        # El operador // hace una división entera (sin decimales)
        # Easy: +1 paquete cada 20 puntos, Medium: +1 paquete cada 30 puntos
        threshold = 20 if self.difficulty == "EASY" else 30
        extra_packages = self.score // threshold

        # 2. La base es 1 paquete + los extra
        total_packages = 1 + extra_packages

        # (Opcional) Ponemos un límite máximo para que el juego no se rompa si tienes 1000 puntos
        # Por ejemplo, máximo 5 paquetes simultáneos.
        if total_packages > 5:
            total_packages = 5

        self.pending_spawns = total_packages

        print(f"--- NUEVA TANDA ---")
        print(f"Puntuación: {self.score}")
        print(f"Dificultad: {self.difficulty} (umbral: {threshold})")
        print(f"Paquetes a generar: {self.pending_spawns}")

        self.spawn_timer = 0  # El primero sale inmediatamente

    def spawn_logic(self):
        """Gestiona la creación de paquetes con retraso entre ellos"""
        if self.pending_spawns > 0:
            if self.spawn_timer > 0:
                self.spawn_timer -= 1
            else:
                # Crear nuevo paquete con la dificultad actual
                new_package = Package(constants.PACKAGE_START[0], constants.PACKAGE_START[1], 0, False, wait_frames=1, difficulty=self.difficulty)
                self.packages.append(new_package)
                self.pending_spawns -= 1
                # Si quedan más paquetes por salir, poner el timer (ej. 30 frames = 1 segundo)
                if self.pending_spawns > 0:
                    self.spawn_timer = 40

    def update(self):
        """Executed every frame: input & logic."""
        # To exit the game
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # --- LÓGICA DEL MENÚ ---
        if self.game_state == "MENU":
            # Navegación del menú (arriba/abajo para Play/Quit)
            if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
                self.menu_selection = 0  # Play
            if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S):
                self.menu_selection = 1  # Quit
            
            # Navegación de dificultad (izquierda/derecha para Easy/Medium)
            if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_A):
                self.difficulty_selection = 0  # Easy
            if pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.KEY_D):
                self.difficulty_selection = 1  # Medium
            
            # Selección del menú
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
                if self.menu_selection == 0:  # Play
                    self.game_state = "PLAYING"
                    # Establecer dificultad según la selección
                    self.difficulty = "EASY" if self.difficulty_selection == 0 else "MEDIUM"
                    self.schedule_new_packages()  # Iniciar el juego con paquetes
                    print(f"¡Juego iniciado en modo {self.difficulty}!")
                elif self.menu_selection == 1:  # Quit
                    pyxel.quit()
            
            return  # No ejecutar el resto de la lógica del juego

        # --- LÓGICA DE CONGELACIÓN (BOSS REGAÑANDO) ---
        if self.is_frozen:
            self.freeze_timer -= 1
            self.boss.animate() # Animar al boss mientras está congelado
            
            if self.freeze_timer <= 0:
                self.is_frozen = False
                self.boss.hide()
                
                # Lógica de fin de vida o reinicio después de la animación
                if self.lives <= 0:
                    print("\n¡GAME OVER! Has perdido todas las vidas")
                    pyxel.quit()
                else:
                    self.packages = []
                    self.schedule_new_packages()
            
            return # DETENER EL RESTO DEL JUEGO

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

        # --- Gestión del boss (contador para ocultarlo después de un tiempo) ---
        if self.boss_display_frames > 0:
            self.boss_display_frames -= 1
            if self.boss_display_frames == 0:
                self.boss.hide()

        # --- Actualizar camión ---
        self.truck.update()

        # --- Actualizar contador de descanso ---
        if self.break_time > 0:
            self.break_time -= 1
            if self.break_time == 0:
                print("¡Descanso terminado! Continúa el juego")
                # Mostrar al boss al final del descanso
                self.boss.show()
                self.boss_display_frames = 90  # Mostrar al boss por 3 segundos
            return  # No procesar el paquete durante el descanso

        # --- LÓGICA DE APARICIÓN DE PAQUETES ---
        self.spawn_logic()

        # --- MOVIMIENTO AUTOMÁTICO DEL PAQUETE ---
        #self.package.move_package()
        packages_to_remove = []

        # --- Presentación de Mario y luigi a la clase paquete ---
        try:
            for pkg in self.packages:
                # Movemos cada paquete individualmente
                passed_package = pkg.move_package(self.mario, self.luigi)

                # Lógica de puntuación y camión para CADA paquete
                if passed_package == True:
                    self.score += 1
                    print(f"¡Punto! Puntuación: {self.score}")

                elif passed_package == "to_truck":
                    self.truck.add_package()
                    packages_to_remove.append(pkg)  # Marcar para borrar
                    print(f"¡Paquete al camión! ({self.truck.packages_count}/8)")
                    
                    # Recuperación de vida en modo MEDIUM
                    if self.difficulty == "MEDIUM":
                        self.deliveries_count += 1
                        if self.deliveries_count >= 5:
                            self.deliveries_count = 0  # Reiniciar contador
                            if self.lives < 3:
                                self.lives += 1
                                print(f"¡VIDA RECUPERADA! Vidas actuales: {self.lives}")
                            else:
                                print("¡BONUS! Vidas al máximo")

                    # Si el camión se llenó
                    if self.truck.is_full():
                        self.score += 10
                        self.break_time = 300
                        print(f"¡Camión lleno! +10 puntos. Puntuación: {self.score}")
                        print("Descanso de 10 segundos...")
                        self.packages = []  # Limpiamos paquetes en pantalla durante el descanso
                        return  # Salimos del update

                    # Si NO se llenó el camión y NO quedan paquetes en cola ni en pantalla...
                    # Lanzamos la siguiente tanda.
                    # Nota: Verificamos si es el último paquete activo para no lanzar infinitos
                    if len(self.packages) - len(packages_to_remove) == 0 and self.pending_spawns == 0:
                        self.schedule_new_packages()

                # Chequeo de colisiones extra (seguridad)
                pkg.check_collision_package(self.mario, self.luigi)

                # Eliminar paquetes que llegaron al camión
            for pkg in packages_to_remove:
                if pkg in self.packages:
                    self.packages.remove(pkg)

                # Si se acabaron los paquetes de la pantalla y no hay pendientes (caso raro de sincronización)
            if len(self.packages) == 0 and self.pending_spawns == 0 and self.break_time == 0:
                self.schedule_new_packages()
        except RuntimeError as e:
            # Se cayó un paquete
            print(f"\n{e}")
            self.lives -= 1
            print(f"Vidas restantes: {self.lives}\n")
            
            # Determinar quién falló para posicionar al boss
            # pkg es la variable del bucle for, que mantiene su valor (el paquete que falló)
            culprit = "mario" # Default
            
            # Lógica para determinar culpable
            # Index 0 (39) -> Luigi
            # Index 1 (50) -> Mario
            # Index 2 (61) -> Luigi
            # Index 3 (72) -> Mario
            # Index 4 (83) -> Depende de X
            
            if pkg.current_y_index == 0 or pkg.current_y_index == 2:
                culprit = "luigi"
            elif pkg.current_y_index == 1 or pkg.current_y_index == 3:
                culprit = "mario"
            elif pkg.current_y_index == 4:
                if pkg.x > 204:
                    culprit = "mario"
                else:
                    culprit = "luigi"
            
            # Posicionar boss
            if culprit == "mario":
                self.boss.x = constants.MARIO_FAIL[0]
                self.boss.y = constants.MARIO_FAIL[1]
                self.boss.flipped = True  # Voltear el sprite para Mario
            else:
                self.boss.x = constants.LUIGI_FAIL[0]
                self.boss.y = constants.LUIGI_FAIL[1]
                self.boss.flipped = False  # No voltear para Luigi

            # Mostrar al boss regañando
            self.boss.show()
            # self.boss_display_frames = 90  # YA NO SE USA, ahora usamos freeze_timer
            
            # ACTIVAR CONGELACIÓN
            self.is_frozen = True
            self.freeze_timer = 60 # 2 segundos a 30 fps

        #self.package.check_collision_package(self.mario, self.luigi)


    def draw(self):
        """Executed every frame: render."""
        # Erasing the previous screen
        pyxel.cls(0)
        
        # --- DIBUJAR MENÚ ---
        if self.game_state == "MENU":
            # Fondo degradado (simulado con rectángulos)
            pyxel.cls(1)  # Fondo azul oscuro base
            
            # Añadir efecto de "estrellas" o puntos decorativos
            for i in range(20):
                x = (i * 13 + pyxel.frame_count // 2) % self.width
                y = (i * 17) % self.height
                pyxel.pset(x, y, 12)  # Puntos azul claro
            
            # Caja decorativa para el título
            title_box_x = self.width // 2 - 60
            title_box_y = 20
            title_box_w = 120
            title_box_h = 25
            
            # Sombra de la caja
            pyxel.rect(title_box_x + 2, title_box_y + 2, title_box_w, title_box_h, 0)
            # Caja principal
            pyxel.rect(title_box_x, title_box_y, title_box_w, title_box_h, 8)
            # Borde de la caja
            pyxel.rectb(title_box_x, title_box_y, title_box_w, title_box_h, 10)
            pyxel.rectb(title_box_x + 1, title_box_y + 1, title_box_w - 2, title_box_h - 2, 9)
            
            # Título del juego con sombra
            title = "MARIO BROS"
            title_x = (self.width - len(title) * 4) // 2
            pyxel.text(title_x + 1, 28, title, 0)  # Sombra
            pyxel.text(title_x, 27, title, 10)  # Texto principal
            
            # Subtítulo
            subtitle = "FACTORY EDITION"
            subtitle_x = (self.width - len(subtitle) * 4) // 2
            pyxel.text(subtitle_x, 37, subtitle, 9)
            
            # Caja para las opciones
            options_box_x = self.width // 2 - 40
            options_box_y = 55
            options_box_w = 80
            options_box_h = 35
            
            # Sombra de la caja de opciones
            pyxel.rect(options_box_x + 2, options_box_y + 2, options_box_w, options_box_h, 0)
            # Caja principal
            pyxel.rect(options_box_x, options_box_y, options_box_w, options_box_h, 5)
            # Borde
            pyxel.rectb(options_box_x, options_box_y, options_box_w, options_box_h, 7)
            
            # Opciones del menú con mejor estilo
            play_y = 62
            quit_y = 77
            
            # Resaltar opción seleccionada con un rectángulo
            if self.menu_selection == 0:
                # Rectángulo de selección para PLAY
                pyxel.rect(options_box_x + 5, play_y - 2, options_box_w - 10, 10, 8)
                pyxel.rectb(options_box_x + 5, play_y - 2, options_box_w - 10, 10, 10)
                play_color = 7  # Blanco
                quit_color = 13  # Gris
            else:
                # Rectángulo de selección para QUIT
                pyxel.rect(options_box_x + 5, quit_y - 2, options_box_w - 10, 10, 8)
                pyxel.rectb(options_box_x + 5, quit_y - 2, options_box_w - 10, 10, 10)
                play_color = 13  # Gris
                quit_color = 7  # Blanco
            
            # Texto de las opciones centrado
            play_text = "PLAY"
            quit_text = "QUIT"
            play_x = (self.width - len(play_text) * 4) // 2
            quit_x = (self.width - len(quit_text) * 4) // 2
            
            pyxel.text(play_x, play_y, play_text, play_color)
            pyxel.text(quit_x, quit_y, quit_text, quit_color)
            
            # Indicador animado (flecha que pulsa)
            indicator_offset = (pyxel.frame_count // 10) % 2  # Animación de pulsación
            indicator_y = play_y if self.menu_selection == 0 else quit_y
            indicator_x = self.width // 2 - 30 - indicator_offset
            pyxel.text(indicator_x, indicator_y, ">", 10)
            
            # Selección de dificultad
            diff_y = 95
            diff_label = "DIFFICULTY:"
            diff_label_x = (self.width - len(diff_label) * 4) // 2
            pyxel.text(diff_label_x, diff_y, diff_label, 6)
            
            # Mostrar Easy y Medium con indicadores
            easy_text = "EASY"
            medium_text = "MEDIUM"
            easy_x = self.width // 2 - 30
            medium_x = self.width // 2 + 10
            
            # Colorear según selección
            easy_color = 10 if self.difficulty_selection == 0 else 13
            medium_color = 10 if self.difficulty_selection == 1 else 13
            
            pyxel.text(easy_x, diff_y + 10, easy_text, easy_color)
            pyxel.text(medium_x, diff_y + 10, medium_text, medium_color)
            
            # Flechas indicadoras <  >
            if self.difficulty_selection == 0:
                pyxel.text(easy_x - 8, diff_y + 10, "<", 10)
                pyxel.text(easy_x + len(easy_text) * 4 + 2, diff_y + 10, ">", 10)
            else:
                pyxel.text(medium_x - 8, diff_y + 10, "<", 10)
                pyxel.text(medium_x + len(medium_text) * 4 + 2, diff_y + 10, ">", 10)
            
            return  # No dibujar el resto del juego
        
        # --- DIBUJAR JUEGO (solo si game_state == "PLAYING") ---
        # Dibuja el fondo PRIMERO (desde Banco 1)
        pyxel.blt(self.background.x, self.background.y, *self.background.sprite)
        # Drawing Mario (x, y, *sprite)
        pyxel.blt(self.mario.x, self.mario.y, *self.mario.sprite)
        # Drawing Luigi (x, y, *sprite)
        pyxel.blt(self.luigi.x, self.luigi.y, *self.luigi.sprite)
        # Drawing Package (x, y, *sprite)
        #pyxel.blt(self.package.x, self.package.y, *self.package.sprite)
        for pkg in self.packages:
            if pkg.package_visible():
                pkg.draw()
            #print("numero de paquetes actuales:", str(len(self.packages)))
        # Drawing Truck (x, y, *sprite)
        pyxel.blt(self.truck.x, self.truck.y, *self.truck.sprite)
        
        # Drawing Boss (solo si es visible)
        if self.boss.is_visible:
            # Si el boss está volteado (Mario falló), usar ancho negativo
            img, u, v, w, h = self.boss.sprite
            if self.boss.flipped:
                # Voltear horizontalmente usando ancho negativo
                pyxel.blt(self.boss.x, self.boss.y, img, u, v, -w, h)
            else:
                pyxel.blt(self.boss.x, self.boss.y, img, u, v, w, h)
            # Mostrar mensaje de regaño

        
        # Mostrar vidas en pantalla
        #pyxel.text(5, 5, f"VIDAS: {self.lives}", 7)
        for i in range(self.lives):
            pyxel.blt(225 + i * 15, 20, *constants.LIVE_SPRITE)

        # Mostrar puntuación en pantalla
        pyxel.text(10, 5, f"PUNTOS: {self.score}", 7)
        # Mostrar paquetes en camión
        #pyxel.text(5, 21, f"CAMION: {self.truck.packages_count}/8", 7)

        truck_offset_x = self.truck.x - constants.TRUCK_START[0]
        limit = min(self.truck.packages_count, 8)
        for i in range(limit):
            # Obtenemos la coordenada base de constants
            base_x, base_y = constants.TRUCK_PACKAGE_POSITIONS[i]

            # Dibujamos sumando el desplazamiento del camión al X (usando el sprite final)
            pyxel.blt(base_x + truck_offset_x, base_y, *constants.PACKAGE_SPRITE_3)

        
        # Mostrar mensaje de descanso si está activo
        if self.break_time > 0:
            seconds_left = self.break_time // 30
            pyxel.text(100, 50, f"DESCANSO: {seconds_left}s", 10)


        # prueba
        #pyxel.blt(36, 60, *self.package.sprite) # 1
        #pyxel.blt(41, 60, *self.package.sprite) # 2
        #pyxel.blt(36, 56, *self.package.sprite) # 3
        #pyxel.blt(41, 56, *self.package.sprite) # 4
        #pyxel.blt(36, 52, *self.package.sprite) # 5
        #pyxel.blt(41, 52, *self.package.sprite) # 6
        #pyxel.blt(36, 48, *self.package.sprite) # 7
        #pyxel.blt(41, 48, *self.package.sprite) # 8

