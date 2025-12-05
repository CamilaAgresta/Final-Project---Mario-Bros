"""
Package Class
"""

import constants
import pyxel

class Package:
    def __init__(self, x: int, y: int, dir: int, at_truck: bool, wait_frames: int = 2, difficulty: str = "EASY", conveyor_speeds: dict = None):
        """
        Creates the Package object.
        :param x: The initial x coordinate
        :param y: The initial y coordinate
        :param dir: Direction (unused currently)
        :param at_truck: Boolean indicating if it's at the truck (unused currently)
        :param wait_frames: Base delay frames for movement speed
        :param difficulty: Game difficulty level
        :param conveyor_speeds: Dictionary of custom speeds for CRAZY mode
        """
        self.x = x
        self.y = y
        self.dir = dir
        self.wait_frames = constants.PACKAGE_WAIT_FRAMES
        self.difficulty = difficulty
        self.conveyor_speeds = conveyor_speeds if conveyor_speeds else {}
        self.move_accumulator = 0.0  # Accumulator for fractional movement (Crazy mode)
        self.sprite = constants.PACKAGE_SPRITE_1  # Start with the first sprite

        self.is_falling = False  # Flag to know if it is falling
        self.fall_start_frame = None  # Frame when it started falling
        self.fall_frame_counter = 0  # Counter to slow down the fall

        self.y_positions = constants.PACKAGE_Y_POSITIONS
        self.current_y_index = self.y_positions.index(y)
        
        # Counter for times passed through invisible zone
        self.invisible_count = 0
        self.was_invisible = False  # To detect when it leaves the invisible zone

    # Properties and setters
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
            raise TypeError("The x must be an integer, " + str(type(x)) + " provided")
        elif x < 0:
            raise ValueError("The x must be a non-negative number")
        else:
            self.__x = x

    @y.setter
    def y(self, y: int):
        if not isinstance(y, int):
            raise TypeError("The y must be an integer, " + str(type(y)) + " provided")
        elif y < 0:
            raise ValueError("The y must be a non-negative number")
        else:
            self.__y = y

    @dir.setter
    def dir(self, dir: int):
        if not isinstance(dir, int):
            raise TypeError("The dir must be an integer, " + str(type(dir)) + " provided")
        elif dir < 0:
            raise ValueError("The dir must be a non-negative number")
        else:
            self.__dir = dir

    def package_visible(self):
        """Determines if the package is visible and changes the sprite when leaving the invisible zone."""
        
        # Invisible zone defined in constants
        start_invisible = constants.INVISIBLE_ZONE_X[0]
        end_invisible = constants.INVISIBLE_ZONE_X[1]
        
        # Is it completely inside the invisible zone?
        is_fully_invisible = (self.x > start_invisible and self.x + self.sprite[3] < end_invisible)
        
        # Detect when it enters TOTALLY invisible zone
        if not hasattr(self, 'was_fully_invisible'):
            self.was_fully_invisible = False

        if not self.was_fully_invisible and is_fully_invisible:
            # Just entered completely into the invisible zone
            self.invisible_count += 1
            
            # Change sprite NOW, so when it comes out it has the new one
            if self.invisible_count == 1:
                self.sprite = constants.PACKAGE_SPRITE_2
            elif self.invisible_count >= 2:
                self.sprite = constants.PACKAGE_SPRITE_3
        
        # Update state for next time
        self.was_fully_invisible = is_fully_invisible
        
        return not is_fully_invisible

    def draw(self):
        """Draws the package with clipping if it is entering/leaving the invisible zone."""
        img = self.sprite[0]
        u = self.sprite[1]
        v = self.sprite[2]
        w = self.sprite[3]
        h = self.sprite[4]
        
        start_invisible = constants.INVISIBLE_ZONE_X[0]
        end_invisible = constants.INVISIBLE_ZONE_X[1]
        
        # Case 1: Fully visible (outside the zone and its edges)
        if self.x + w <= start_invisible or self.x >= end_invisible:
            pyxel.blt(self.x, self.y, img, u, v, w, h)
            
        # Case 2: Entering the invisible zone (right side clipped)
        elif self.x < start_invisible < self.x + w:
            visible_w = start_invisible - self.x
            pyxel.blt(self.x, self.y, img, u, v, visible_w, h)
            
        # Case 3: Leaving the invisible zone (left side clipped)
        elif self.x < end_invisible < self.x + w:
            visible_w = (self.x + w) - end_invisible
            draw_x = end_invisible
            skip_w = w - visible_w
            pyxel.blt(draw_x, self.y, img, u + skip_w, v, visible_w, h)
            
        # Case 4: Fully inside (nothing drawn)
        else:
            pass

    def fall(self):
        """Handles the package falling animation when not caught."""
        if not self.is_falling:
            self.is_falling = True
            self.fall_start_frame = pyxel.frame_count
            self.fall_frame_counter = 0
        
        # Calculate time elapsed since falling started (in seconds)
        frames_falling = pyxel.frame_count - self.fall_start_frame
        time_falling = frames_falling / 30.0
        
        # If falling for more than 0.5 seconds, raise error
        if time_falling > 0.5:
            raise RuntimeError(f"PACKAGE LOST! The package fell without being caught at x={self.x}, y={self.y}")
        
        # Fall slower: only update Y every 2 frames
        self.fall_frame_counter += 1
        if self.fall_frame_counter >= 2:
            self.y += 1
            self.fall_frame_counter = 0

    def check_collision_package(self, mario, luigi):
        """Checks for collisions with conveyors or characters."""
        
        # Helper variables for clarity
        conveyor_y_0 = constants.CONVEYOR_Y[0] # 83
        conveyor_y_1 = constants.CONVEYOR_Y[1] # 72
        conveyor_y_2 = constants.CONVEYOR_Y[2] # 61
        conveyor_y_3 = constants.CONVEYOR_Y[3] # 50
        conveyor_y_4 = constants.CONVEYOR_Y[4] # 39

        # PACKAGE ON CONVEYOR
        # CONVEYOR 0 - right side (before Mario)
        if (self.y == conveyor_y_0 and constants.CONVEYOR_0_X < self.x):
            return "package in conveyor"
        # CONVEYOR 1 - left side (after Mario)
        elif (self.y == conveyor_y_0 and constants.CONVEYOR_ODD_X[0] <= self.x <= constants.CONVEYOR_ODD_X[1]):
            return "package in conveyor"
        # Other conveyors
        elif (((self.y == conveyor_y_1 or self.y == conveyor_y_3) and constants.CONVEYOR_EVEN_X[0] <= self.x <= constants.CONVEYOR_EVEN_X[1]) or
              ((self.y == conveyor_y_2 or self.y == conveyor_y_4) and constants.CONVEYOR_ODD_X[0] <= self.x <= constants.CONVEYOR_ODD_X[1])):
            return "package in conveyor"

        # MARIO - detects when package leaves right side of conveyors
        # Mario catches at: Y positions 2 (83), 1 (61), 0 (39) corresponding to conveyors 0, 2, 4 (indices)
        # But wait, Mario Y positions are (39, 61, 83).
        # Index 2 is 83 -> Conveyor 0 (y=83)
        # Index 1 is 61 -> Conveyor 2 (y=61)
        # Index 0 is 39 -> Conveyor 4 (y=39) -- Wait, Conveyor 4 is y=50? No.
        # Let's check constants:
        # CONVEYOR_Y = (83, 72, 61, 50, 39) -> indices 0, 1, 2, 3, 4
        # Mario Y positions: (39, 61, 83)
        # Mario at 83 catches from Conveyor 0 (index 0, y=83)
        # Mario at 61 catches from Conveyor 2 (index 2, y=61)
        # Mario at 39 catches from Conveyor 4 (index 4, y=39)
        
        # Refactored collision logic for Mario
        mario_catch_y = [constants.CONVEYOR_Y[0], constants.CONVEYOR_Y[2], constants.CONVEYOR_Y[4]] # 83, 61, 39
        
        if (mario.y == constants.MARIO_Y_POSITIONS[2] and constants.CONVEYOR_ODD_X[1] <= self.x <= constants.CONVEYOR_0_X and abs(self.y - constants.CONVEYOR_Y[0]) <= 8) or \
           (mario.y == constants.MARIO_Y_POSITIONS[1] and self.x >= constants.CONVEYOR_EVEN_X[1] and abs(self.y - constants.CONVEYOR_Y[1]) <= 8) or \
           (mario.y == constants.MARIO_Y_POSITIONS[0] and self.x >= constants.CONVEYOR_EVEN_X[1] and abs(self.y - constants.CONVEYOR_Y[3]) <= 8):
             return "collision mario"

        # LUIGI - detects when package leaves left side of conveyors
        elif ((luigi.y == constants.LUIGI_Y_POSITIONS[2] and self.x <= constants.CONVEYOR_ODD_X[0] and abs(self.y - constants.CONVEYOR_Y[0]) <= 8) or
              (luigi.y == constants.LUIGI_Y_POSITIONS[1] and self.x <= constants.CONVEYOR_ODD_X[0] and abs(self.y - constants.CONVEYOR_Y[2]) <= 8) or
              (luigi.y == constants.LUIGI_Y_POSITIONS[0] and self.x <= constants.CONVEYOR_ODD_X[0] and abs(self.y - constants.CONVEYOR_Y[4]) <= 8)):
            return "collision luigi"
        else:
            return "no collision"

    def _get_speed_multiplier(self, is_conveyor_0, is_odd_conveyor, is_even_conveyor):
        """Helper to calculate speed multiplier based on difficulty and conveyor type."""
        if self.difficulty == "CRAZY":
            if is_conveyor_0:
                return 1.0
            return self.conveyor_speeds.get(self.current_y_index, 1.0)
            
        elif self.difficulty == "EXTREME":
            if is_odd_conveyor: return 2.0  # 2x speed
            if is_even_conveyor: return 1.5 # 1.5x speed
            return 1.0 # Conveyor 0 normal
            
        elif self.difficulty == "MEDIUM":
            if is_odd_conveyor: return 1.5
            return 1.0
            
        else: # EASY
            return 1.0

    def move_package(self, mario, luigi):
        """Moves the package horizontally and handles transfers between conveyors."""

        # Identify conveyor type
        is_conveyor_0 = (self.current_y_index == 4 and self.x > constants.CONVEYOR_0_X)
        is_odd_conveyor = (self.current_y_index in [0, 2]) or (self.current_y_index == 4 and constants.CONVEYOR_ODD_X[0] <= self.x <= constants.CONVEYOR_ODD_X[1])
        is_even_conveyor = (self.current_y_index in [1, 3])
        
        multiplier = self._get_speed_multiplier(is_conveyor_0, is_odd_conveyor, is_even_conveyor)
        
        # Logic for movement based on multiplier
        should_move = False
        
        if self.difficulty == "CRAZY":
            speed = 0.5 * multiplier
            self.move_accumulator += speed
            if self.move_accumulator >= 1.0:
                self.move_accumulator -= 1.0
                should_move = True
        else:
            # For standard difficulties, we use frame skipping logic to simulate speed
            if multiplier == 2.0: # Every frame
                should_move = True
            elif multiplier == 1.5: # 2 out of 3 frames
                should_move = (pyxel.frame_count % 3 != 0)
            else: # 1.0 (Normal speed, every wait_frames)
                should_move = (pyxel.frame_count % self.wait_frames == 0)

        if not should_move:
            return False

        # Collision check
        collision_status = self.check_collision_package(mario, luigi)

        # --- CONVEYOR 0 (Right side, y=83) ---
        if self.current_y_index == 4 and self.x > constants.CONVEYOR_ODD_X[1]:
            if collision_status == "package in conveyor":
                self.is_falling = False
                self.fall_start_frame = None
                self.x -= 1
            elif collision_status == "collision mario":
                self.is_falling = False
                self.fall_start_frame = None
                self.x = constants.CONVEYOR_ODD_X[1]
                self.y = constants.CONVEYOR_Y[0]
                return True
            else:
                self.fall()

        # --- CONVEYOR 1 (Left side, y=83) ---
        elif self.current_y_index == 4 and self.x <= constants.CONVEYOR_ODD_X[1]:
            if collision_status == "package in conveyor":
                self.is_falling = False
                self.fall_start_frame = None
                self.x -= 1
            elif collision_status == "collision luigi":
                self.is_falling = False
                self.fall_start_frame = None
                self.y = self.y_positions[self.current_y_index-1]
                self.current_y_index -= 1
                self.x = constants.CONVEYOR_EVEN_X[0]
                return True
            else:
                self.fall()

        # --- CONVEYOR 2 and 4 (Even indices in list logic, but odd in Y position list indices 1 and 3) ---
        elif self.current_y_index == 3 or self.current_y_index == 1:
            if collision_status == "package in conveyor":
                self.is_falling = False
                self.fall_start_frame = None
                self.x += 1
            elif collision_status == "collision mario":
                self.is_falling = False
                self.fall_start_frame = None
                self.y = self.y_positions[self.current_y_index-1]
                self.current_y_index -= 1
                self.x = constants.CONVEYOR_ODD_X[1]
                return True
            else:
                self.fall()

        # --- CONVEYOR 3 (Index 2) ---
        elif self.current_y_index == 2:
            if collision_status == "package in conveyor":
                self.is_falling = False
                self.fall_start_frame = None
                self.x -= 1
            elif collision_status == "collision luigi":
                self.is_falling = False
                self.fall_start_frame = None
                self.y = self.y_positions[self.current_y_index-1]
                self.current_y_index -= 1
                self.x = constants.CONVEYOR_EVEN_X[0]
                return True
            else:
                self.fall()

        # --- CONVEYOR 5 (Last one, Index 0) ---
        elif self.current_y_index == 0:
            if collision_status == "package in conveyor":
                self.is_falling = False
                self.fall_start_frame = None
                self.x -= 1
            elif collision_status == "collision luigi":
                return "to_truck"
            else:
                self.fall()
        
        return False
