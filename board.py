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
        self.boss = Boss(constants.BOSS_START[0], constants.BOSS_START[1])

        # Sistema de vidas
        self.lives = 3
        self.boss_display_frames = 0  # Contador para mostrar al boss temporalmente
        self.score = 0  # Puntuación del juego
        self.break_time = 0  # Contador para el descanso cuando el camión se llena

        # System of packages
        self.packages = []

        # Variables para controlar la aparición (spawn) de paquetes
        self.pending_spawns = 0  # Cuántos paquetes quedan por salir en esta tanda
        self.spawn_timer = 0  # Temporizador para el retraso entre paquetes
        self.schedule_new_packages()  # Iniciamos el primer paquete




        # Initialization pyxel
        pyxel.init(self.width, self.height, title = "Mario Bros")
        # Loading the pyxres file with the images
        # AGREGAR CARPETAS DIFERENTES DENTRO DE ASSATS PARA PERSONAJES - FONDO - LABERINTO
        pyxel.load("assets/characters.pyxres")
        #pyxel.load("assets/fondo.pyxres")

        # Running the game
        pyxel.run(self.update, self.draw)

    def schedule_new_packages(self):
        """Calcula cuántos paquetes lanzar según la puntuación"""

        # 1. Calculamos cuántos grupos de 50 llevamos
        # El operador // hace una división entera (sin decimales)
        extra_packages = self.score // 20

        # 2. La base es 1 paquete + los extra por cada 50 puntos
        total_packages = 1 + extra_packages

        # (Opcional) Ponemos un límite máximo para que el juego no se rompa si tienes 1000 puntos
        # Por ejemplo, máximo 5 paquetes simultáneos.
        if total_packages > 5:
            total_packages = 5

        self.pending_spawns = total_packages

        print(f"--- NUEVA TANDA ---")
        print(f"Puntuación: {self.score}")
        print(f"Nivel de dificultad: {extra_packages}")
        print(f"Paquetes a generar: {self.pending_spawns}")

        self.spawn_timer = 0  # El primero sale inmediatamente

    def spawn_logic(self):
        """Gestiona la creación de paquetes con retraso entre ellos"""
        if self.pending_spawns > 0:
            if self.spawn_timer > 0:
                self.spawn_timer -= 1
            else:
                # Crear nuevo paquete
                new_package = Package(constants.PACKAGE_START[0], constants.PACKAGE_START[1], 0, False, wait_frames=1)
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
            
            # Mostrar al boss regañando
            self.boss.show()
            self.boss_display_frames = 90  # Mostrar al boss por 3 segundos (90 frames a 30 fps)
            
            if self.lives <= 0:
                print("\n¡GAME OVER! Has perdido todas las vidas")
                pyxel.quit()
            else:
                # Reiniciar el paquete en la posición inicial
                #self.package = Package(constants.PACKAGE_START[0], constants.PACKAGE_START[1], 0, False, wait_frames = 1)
                self.packages = []
                self.schedule_new_packages()

        #self.package.check_collision_package(self.mario, self.luigi)


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
        #pyxel.blt(self.package.x, self.package.y, *self.package.sprite)
        for pkg in self.packages:
            if pkg.package_visible():
                pyxel.blt(pkg.x, pkg.y, *pkg.sprite)
            #print("numero de paquetes actuales:", str(len(self.packages)))
        # Drawing Truck (x, y, *sprite)
        pyxel.blt(self.truck.x, self.truck.y, *self.truck.sprite)
        
        # Drawing Boss (solo si es visible)
        if self.boss.is_visible:
            pyxel.blt(self.boss.x, self.boss.y, *self.boss.sprite)
            # Mostrar mensaje de regaño
            pyxel.text(self.boss.x - 20, self.boss.y - 10, "¡CUIDADO!", 8)
        
        # Mostrar vidas en pantalla
        #pyxel.text(5, 5, f"VIDAS: {self.lives}", 7)
        for i in range(self.lives):
            pyxel.blt(225 + i * 15, 20, *constants.LIVE_SPRITE)

        # Mostrar puntuación en pantalla
        pyxel.text(10, 5, f"PUNTOS: {self.score}", 7)
        # Mostrar paquetes en camión
        pyxel.text(5, 21, f"CAMION: {self.truck.packages_count}/8", 7)
        
        # Mostrar mensaje de descanso si está activo
        if self.break_time > 0:
            seconds_left = self.break_time // 30
            pyxel.text(100, 50, f"DESCANSO: {seconds_left}s", 10)


        # prueba
        pyxel.blt(162, 100, *self.package.sprite)

