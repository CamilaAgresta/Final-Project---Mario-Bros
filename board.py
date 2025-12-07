"""
Board Class
Main game logic and loop
"""

import pyxel
import random
import constants
from background import Background
from character import Character
from mario import Mario
from luigi import Luigi
from package import Package
from truck import Truck
from boss import Boss


class Board:
    """This class contains the game board and main logic."""

    def __init__(self, width: int, height: int):
        """
        Creates the board and initializes the game.
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
        self.truck = Truck(constants.TRUCK_START[0], constants.TRUCK_START[1])
        self.boss_right = Boss(constants.MARIO_FAIL[0], constants.MARIO_FAIL[1])
        self.boss_left = Boss(constants.LUIGI_FAIL[0], constants.LUIGI_FAIL[1])
        self.boss_right.flipped = True  # Mario side (right) needs flip
        self.boss_left.flipped = False  # Luigi side (left) normal

        # Life system
        self.lives = 3
        self.life_blink_timer = 0  # Timer for lost life blinking
        self.life_being_lost = False  # If a life is being lost (blinking active)
        self.boss_display_frames = 0  # Timer to show boss temporarily
        self.score = 0  # Game score
        self.break_time = 0  # Timer for break when truck is full
        self.is_frozen = False  # Game freeze state
        self.freeze_timer = 0  # Timer for freeze
        
        # Game state management
        self.game_state = "MENU"  # Can be: "MENU", "PLAYING", "GAME_OVER"
        self.menu_selection = 0  # 0 = Play, 1 = Quit
        self.difficulty_selection = 0  # 0 = Easy, 1 = Medium
        self.difficulty = "EASY"  # Set when game starts
        self.consecutive_trucks = 0  # Count of full trucks departing (for life recovery)
        self.conveyor_speeds = {}  # Dictionary for random speeds in CRAZY mode

        # System of packages
        self.packages = []

        # Variables to control package spawning
        self.pending_spawns = 0  # How many packages left to spawn in this batch
        self.spawn_timer = 0  # Timer for delay between packages
        
        # Initialization pyxel
        pyxel.init(self.width, self.height, title="Mario Bros", display_scale=constants.DISPLAY_SCALE)
        
        # Loading assets
        pyxel.load("assets/characters.pyxres")
        
        # Setup Audio
        self.setup_audio()

        # Running the game
        pyxel.run(self.update, self.draw)

    def setup_audio(self):
        """Configures background music (chiptune)."""
        # Channel 0: Main Melody (Square wave)
        pyxel.sounds[0].set(
            notes="c3e3g3e3 c3e3g3a3 f3a3c4a3 f3a3g3r "
                  "e3g3b3g3 e3g3b3c4 d3f3a3f3 d3f3g3r",
            tones="S",
            volumes="6666666666666666" * 2,
            effects="nnnnnnnnnnnnnnnn" * 2,
            speed=12
        )
        
        # Channel 1: Harmony (Triangle wave)
        pyxel.sounds[1].set(
            notes="c2g2c3g2 c2g2c3c3 f2c3f3c3 f2c3e3r "
                  "e2b2e3b2 e2b2e3e3 d2a2d3a2 d2a2g2r",
            tones="T",
            volumes="4444444444444444" * 2,
            effects="nnnnnnnnnnnnnnnn" * 2,
            speed=12
        )
        
        # Channel 2: Bass (Triangle wave)
        pyxel.sounds[2].set(
            notes="c1c1c1c1 c1c1c1c1 f1f1f1f1 f1f1f1r "
                  "e1e1e1e1 e1e1e1e1 d1d1d1d1 d1d1d1r",
            tones="T",
            volumes="5555555555555555" * 2,
            effects="nnnnnnnnnnnnnnnn" * 2,
            speed=12
        )
        
        # Channel 3: Percussion (Noise)
        pyxel.sounds[3].set(
            notes="c1r c1r c1r c1r " * 4,
            tones="N",
            volumes="5353535353535353" * 2,
            effects="nnnnnnnnnnnnnnnn" * 2,
            speed=12
        )
        
        # Music (M0) combining 4 channels
        pyxel.musics[0].set([0], [1], [2], [3])
        
        # Start music loop
        pyxel.playm(0, loop=True)

    def schedule_new_packages(self):
        """Calculates how many packages to launch based on score."""

        # 1. Calculate batches based on difficulty
        if self.difficulty == "CRAZY":
            # Crazy: +2 packages every 20 points
            threshold = 20
            extra_packages = (self.score // threshold) * 2
        else:
            # Easy: +1 package every 20 points, Medium/Extreme: +1 package every 30 points
            threshold = 20 if self.difficulty == "EASY" else 30
            extra_packages = self.score // threshold

        # 2. Base is 1 package + extras
        total_packages = 1 + extra_packages

        # Limit max packages to avoid breaking the game
        if total_packages > 8:
            total_packages = 8

        self.pending_spawns = total_packages
        self.spawn_timer = 0  # First one comes out immediately
        
    def reset_game(self):
        """Resets the game to initial state."""
        self.score = 0
        self.lives = 3
        self.packages = []
        self.pending_spawns = 0
        self.spawn_timer = 0
        self.truck.packages_count = 0
        self.break_time = 0
        self.is_frozen = False
        self.freeze_timer = 0
        self.consecutive_trucks = 0
        self.life_blink_timer = 0
        self.life_being_lost = False
        self.boss_right.hide()
        self.boss_left.hide()
        
        # Generate random speeds for CRAZY
        if self.difficulty == "CRAZY":
            self.conveyor_speeds = {
                0: random.uniform(1.0, 2.0), # Conveyor 5
                1: random.uniform(1.0, 2.0), # Conveyor 4
                2: random.uniform(1.0, 2.0), # Conveyor 3
                3: random.uniform(1.0, 2.0), # Conveyor 2
                4: random.uniform(1.0, 2.0)  # Conveyor 1 (left part)
            }
        else:
            self.conveyor_speeds = {}
            
        self.schedule_new_packages()
        self.game_state = "PLAYING"

    def spawn_logic(self):
        """Manages package creation with delay."""
        if self.pending_spawns > 0:
            if self.spawn_timer > 0:
                self.spawn_timer -= 1
            else:
                # Create new package
                new_package = Package(constants.PACKAGE_START[0], constants.PACKAGE_START[1], wait_frames=1, difficulty=self.difficulty, conveyor_speeds=self.conveyor_speeds)
                self.packages.append(new_package)
                self.pending_spawns -= 1
                # If more packages pending, set timer
                if self.pending_spawns > 0:
                    self.spawn_timer = 70

    def update_menu(self):
        """Handles menu logic."""
        # Menu navigation (Up/Down)
        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
            self.menu_selection = 0  # Play
        if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S):
            self.menu_selection = 1  # Quit
        
        # Difficulty navigation (Left/Right)
        if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_A):
            self.difficulty_selection = (self.difficulty_selection - 1) % 4
        if pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.KEY_D):
            self.difficulty_selection = (self.difficulty_selection + 1) % 4
        
        # Selection
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
            if self.menu_selection == 0:  # Play
                self.game_state = "PLAYING"
                # Set difficulty
                if self.difficulty_selection == 0: self.difficulty = "EASY"
                elif self.difficulty_selection == 1: self.difficulty = "MEDIUM"
                elif self.difficulty_selection == 2: self.difficulty = "EXTREME"
                else: self.difficulty = "CRAZY"
                
                self.reset_game()
            elif self.menu_selection == 1:  # Quit
                pyxel.quit()

    def update_game_over(self):
        """Handles game over logic."""
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_R):
            self.reset_game()
        elif pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def update_playing(self):
        """Handles main game logic."""
        # --- LIFE BLINK LOGIC ---
        if self.life_blink_timer > 0:
            self.life_blink_timer -= 1
            if self.life_blink_timer == 0:
                self.life_being_lost = False
        
        # --- FREEZE LOGIC (BOSS SCOLDING) ---
        if self.is_frozen:
            self.freeze_timer -= 1
            if self.boss_right.is_visible: self.boss_right.animate()
            if self.boss_left.is_visible: self.boss_left.animate()
            if self.freeze_timer <= 0:
                self.is_frozen = False
                self.boss_right.hide()
                self.boss_left.hide()
                
                # If lives reached 0, switch to GAME OVER
                if self.lives <= 0:
                    self.game_state = "GAME_OVER"
                    return
                
                # Reset failed package batch
                self.packages = []
                self.schedule_new_packages()
            return # STOP REST OF GAME UPDATE

        # --- Mario Controls ---
        # Frozen during last 10 seconds of break
        if not (self.break_time > 0 and self.break_time <= 300):
            if pyxel.btnp(pyxel.KEY_UP): self.mario.move_vertical('up')
            if pyxel.btnp(pyxel.KEY_DOWN): self.mario.move_vertical('down')

        # --- Luigi Controls ---
        if not (self.break_time > 0 and self.break_time <= 300):
            if pyxel.btnp(pyxel.KEY_W): self.luigi.move_vertical('up')
            if pyxel.btnp(pyxel.KEY_S): self.luigi.move_vertical('down')

        # --- Boss Management ---
        if self.boss_display_frames > 0:
            self.boss_display_frames -= 1
            if self.boss_right.is_visible: self.boss_right.animate()
            if self.boss_left.is_visible: self.boss_left.animate()
            if self.boss_display_frames == 0:
                self.boss_right.hide()
                self.boss_left.hide()

        # --- Update Truck ---
        self.truck.update()

        # --- Break Time Logic ---
        if self.break_time > 0:
            self.break_time -= 1
            
            # Show bosses when 2 seconds left
            if self.break_time == 60:
                 self.boss_right.show()
                 self.boss_left.show()
                 self.boss_display_frames = 60
                 
            if self.break_time == 0:
                self.boss_right.hide()
                self.boss_left.hide()
                self.boss_display_frames = 0
            return  # Skip package processing during break

        # --- SPAWN LOGIC ---
        self.spawn_logic()

        # --- PACKAGE MOVEMENT ---
        packages_to_remove = []

        try:
            for pkg in self.packages:
                # Move each package
                passed_package = pkg.move_package(self.mario, self.luigi)

                # Scoring and Truck Logic
                if passed_package == True:
                    self.score += 1

                elif passed_package == "to_truck":
                    self.truck.add_package()
                    packages_to_remove.append(pkg)

                    # If truck is full
                    if self.truck.is_full():
                        self.score += 10
                        self.break_time = 300
                        self.packages = []  # Clear packages
                        
                        # --- LIFE RECOVERY LOGIC ---
                        # Only recover life if difficulty is NOT Crazy
                        if self.difficulty != "CRAZY":
                            self.consecutive_trucks += 1
                            
                            # Threshold depends on difficulty
                            threshold = 3 if self.difficulty == "EASY" else 5
                            
                            if self.consecutive_trucks >= threshold:
                                self.consecutive_trucks = 0
                                if self.lives < 3:
                                    self.lives += 1

                        return  # Exit update

                    # If truck NOT full and NO packages left...
                    if len(self.packages) - len(packages_to_remove) == 0 and self.pending_spawns == 0:
                        self.schedule_new_packages()

                # Extra collision check
                pkg.check_collision_package(self.mario, self.luigi)

            # Remove delivered packages
            for pkg in packages_to_remove:
                if pkg in self.packages:
                    self.packages.remove(pkg)

            # If screen empty and no pending spawns
            if len(self.packages) == 0 and self.pending_spawns == 0 and self.break_time == 0:
                self.schedule_new_packages()
                
        except RuntimeError as e:
            # Package fell
            print(f"\n{e}")
            
            # Activate life blink
            self.life_being_lost = True
            self.life_blink_timer = 60
            
            self.lives -= 1
            
            # Determine culprit for boss position
            culprit = "mario" # Default
            
            if pkg.current_y_index == 0 or pkg.current_y_index == 2:
                culprit = "luigi"
            elif pkg.current_y_index == 1 or pkg.current_y_index == 3:
                culprit = "mario"
            elif pkg.current_y_index == 4:
                if pkg.x > 204: culprit = "mario"
                else: culprit = "luigi"
            
            # Position boss
            if culprit == "mario": self.boss_right.show()
            else: self.boss_left.show()

            # ACTIVATE FREEZE
            self.is_frozen = True
            self.freeze_timer = 60

    def update(self):
        """Executed every frame: input & logic."""
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.game_state == "MENU":
            self.update_menu()
        elif self.game_state == "GAME_OVER":
            self.update_game_over()
        else:
            self.update_playing()


    def draw_menu(self):
        """Draws the main menu."""
        pyxel.cls(1)  # Dark blue background
        
        # Stars effect
        for i in range(20):
            x = (i * 13 + pyxel.frame_count // 2) % self.width
            y = (i * 17) % self.height
            pyxel.pset(x, y, 12)
        
        # Title Box
        title_box_x = self.width // 2 - 60
        title_box_y = 20
        title_box_w = 120
        title_box_h = 25
        
        pyxel.rect(title_box_x + 2, title_box_y + 2, title_box_w, title_box_h, 0) # Shadow
        pyxel.rect(title_box_x, title_box_y, title_box_w, title_box_h, 8) # Main
        pyxel.rectb(title_box_x, title_box_y, title_box_w, title_box_h, 10) # Border
        pyxel.rectb(title_box_x + 1, title_box_y + 1, title_box_w - 2, title_box_h - 2, 9)
        
        # Title
        title = "MARIO BROS"
        title_x = (self.width - len(title) * 4) // 2
        pyxel.text(title_x + 1, 28, title, 0)
        pyxel.text(title_x, 27, title, 10)
        
        # Subtitle
        subtitle = "FACTORY EDITION"
        subtitle_x = (self.width - len(subtitle) * 4) // 2
        pyxel.text(subtitle_x, 37, subtitle, 9)
        
        # Options Box
        options_box_x = self.width // 2 - 40
        options_box_y = 55
        options_box_w = 80
        options_box_h = 35
        
        pyxel.rect(options_box_x + 2, options_box_y + 2, options_box_w, options_box_h, 0)
        pyxel.rect(options_box_x, options_box_y, options_box_w, options_box_h, 5)
        pyxel.rectb(options_box_x, options_box_y, options_box_w, options_box_h, 7)
        
        # Options
        play_y = 62
        quit_y = 77
        
        # Selection Highlight
        if self.menu_selection == 0:
            pyxel.rect(options_box_x + 5, play_y - 2, options_box_w - 10, 10, 8)
            pyxel.rectb(options_box_x + 5, play_y - 2, options_box_w - 10, 10, 10)
            play_color = 7
            quit_color = 13
        else:
            pyxel.rect(options_box_x + 5, quit_y - 2, options_box_w - 10, 10, 8)
            pyxel.rectb(options_box_x + 5, quit_y - 2, options_box_w - 10, 10, 10)
            play_color = 13
            quit_color = 7
        
        play_text = "PLAY"
        quit_text = "QUIT"
        play_x = (self.width - len(play_text) * 4) // 2
        quit_x = (self.width - len(quit_text) * 4) // 2
        
        pyxel.text(play_x, play_y, play_text, play_color)
        pyxel.text(quit_x, quit_y, quit_text, quit_color)
        
        # Indicator
        indicator_offset = (pyxel.frame_count // 10) % 2
        indicator_y = play_y if self.menu_selection == 0 else quit_y
        indicator_x = self.width // 2 - 30 - indicator_offset
        pyxel.text(indicator_x, indicator_y, ">", 10)
        
        # Difficulty
        diff_y = 95
        diff_label = "DIFFICULTY:"
        diff_label_x = (self.width - len(diff_label) * 4) // 2
        pyxel.text(diff_label_x, diff_y, diff_label, 6)
        
        easy_text = "EASY"
        medium_text = "MED"
        extreme_text = "EXT"
        crazy_text = "CRAZY"
        
        start_x = self.width // 2 - 60
        easy_x = start_x
        medium_x = start_x + 30
        extreme_x = start_x + 55
        crazy_x = start_x + 80
        
        easy_color = 10 if self.difficulty_selection == 0 else 13
        medium_color = 10 if self.difficulty_selection == 1 else 13
        extreme_color = 10 if self.difficulty_selection == 2 else 13
        crazy_color = 10 if self.difficulty_selection == 3 else 13
        if self.difficulty_selection == 3: crazy_color = 8
        
        pyxel.text(easy_x, diff_y + 10, easy_text, easy_color)
        pyxel.text(medium_x, diff_y + 10, medium_text, medium_color)
        pyxel.text(extreme_x, diff_y + 10, extreme_text, extreme_color)
        pyxel.text(crazy_x, diff_y + 10, crazy_text, crazy_color)
        
        # Difficulty Arrows
        if self.difficulty_selection == 0:
            pyxel.text(easy_x - 8, diff_y + 10, "<", 10)
            pyxel.text(easy_x + len(easy_text) * 4 + 2, diff_y + 10, ">", 10)
        elif self.difficulty_selection == 1:
            pyxel.text(medium_x - 8, diff_y + 10, "<", 10)
            pyxel.text(medium_x + len(medium_text) * 4 + 2, diff_y + 10, ">", 10)
        elif self.difficulty_selection == 2:
            pyxel.text(extreme_x - 8, diff_y + 10, "<", 10)
            pyxel.text(extreme_x + len(extreme_text) * 4 + 2, diff_y + 10, ">", 10)
        else:
            pyxel.text(crazy_x - 8, diff_y + 10, "<", 8)
            pyxel.text(crazy_x + len(crazy_text) * 4 + 2, diff_y + 10, ">", 8)

    def draw_game_over(self):
        """Draws the game over screen."""
        pyxel.cls(0)
        
        game_over_text = "GAME OVER"
        go_x = (self.width - len(game_over_text) * 4) // 2
        go_y = self.height // 2 - 20
        pyxel.text(go_x, go_y, game_over_text, 8)
        
        score_text = f"FINAL SCORE: {self.score}"
        score_x = (self.width - len(score_text) * 4) // 2
        pyxel.text(score_x, go_y + 15, score_text, 7)
        
        restart_text = "PRESS ENTER TO RESTART"
        quit_text = "PRESS Q TO QUIT"
        
        restart_x = (self.width - len(restart_text) * 4) // 2
        quit_x = (self.width - len(quit_text) * 4) // 2
        
        color_blink = 10 if (pyxel.frame_count // 15) % 2 == 0 else 7
        
        pyxel.text(restart_x, go_y + 35, restart_text, color_blink)
        pyxel.text(quit_x, go_y + 45, quit_text, 13)

    def draw_playing(self):
        """Draws the game elements."""
        # Draw background
        pyxel.blt(self.background.x, self.background.y, *self.background.sprite)
        
        # Draw Characters
        self.mario.draw()
        self.luigi.draw()
        
        # Draw Packages
        for pkg in self.packages:
            if pkg.package_visible():
                pkg.draw()
        
        # Draw Truck
        self.truck.draw()
        
        # Draw Bosses
        self.boss_right.draw()
        self.boss_left.draw()
        
        # Draw Lives
        for i in range(self.lives):
            pyxel.blt(225 + i * 15, 20, *constants.LIVE_SPRITE)

        # Blinking life
        if self.life_being_lost and self.life_blink_timer > 0:
            if (self.life_blink_timer // 5) % 2 == 0:
                pyxel.blt(225 + self.lives * 15, 20, *constants.LIVE_SPRITE)

        # Draw Score
        pyxel.text(10, 5, f"POINTS: {self.score}", 7)
        
        # Draw Break Message
        if self.break_time > 0:
            seconds_left = self.break_time // 30
            break_text = f"BREAK: {seconds_left}s"
            text_x = (self.width - len(break_text) * 4) // 2
            pyxel.text(text_x, 5, break_text, 10)

    def draw(self):
        """Executed every frame: render."""
        pyxel.cls(0)
        
        if self.game_state == "MENU":
            self.draw_menu()
        elif self.game_state == "GAME_OVER":
            self.draw_game_over()
        else:
            self.draw_playing()

