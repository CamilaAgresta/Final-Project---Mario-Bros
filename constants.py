"""
Final Project: Super Mario Bros
Constants
"""

# Tuple meaning for XXX_SPRITE
# The tuple is (bank_img, x_in_bank, y_in_bank, width, height)

# ---------------------------------
# Dimension of the screen
WIDTH = 288
HIGH = 118
DISPLAY_SCALE = 8  # Increased for larger screen

# ---------------------------------
# Background
BACKGROUND_START = (16, 16)
BACKGROUND_SPRITE = (1, 0, 0, 256, 100)
INVISIBLE_ZONE_X = (125, 162)

# ---------------------------------
# MARIO
MARIO_START = (215, 83)
MARIO_SPRITE = (0, 0, 0, 12, 16)  # 12 width x 16 height, Mario occupies the first quadrant

# Allowed Y positions for Mario (from top to bottom: 39, 61, 83)
MARIO_Y_POSITIONS = (39, 61, 83)

# ---------------------------------
# LUIGI
LUIGI_START = (60, 72)
LUIGI_SPRITE = (0, 0, 16, 12, 16)
# Allowed Y positions for Luigi (from top to bottom: 28, 50, 72)
LUIGI_Y_POSITIONS = (28, 50, 72)

# ---------------------------------
# CONVEYOR
CONVEYOR_0_X = 229
CONVEYOR_ODD_X = (83, 204)
CONVEYOR_EVEN_X = (80, 201)

CONVEYOR_Y = (83, 72, 61, 50, 39)

# ---------------------------------
# PACKAGE
PACKAGE_START = (260, 83)  # Starts at CONVEYOR 0 (right side, 2 pixels higher)

# Package sprites (change when passing through invisible zones)
PACKAGE_SPRITE_1 = (0, 27, 6, 11, 5)   # Initial sprite
PACKAGE_SPRITE_2 = (0, 27, 14, 11, 5)  # Sprite after 1st time invisible
PACKAGE_SPRITE_3 = (0, 29, 22, 7, 5)   # Sprite after 2nd time invisible

# Default sprite (for compatibility)
PACKAGE_SPRITE = PACKAGE_SPRITE_1

# Y positions of the conveyor belts
# IMPORTANT: CONVEYOR 0 and CONVEYOR 1 share the same Y (85) but different X ranges
PACKAGE_Y_POSITIONS = (39, 50, 61, 72, 83)  # 5 different heights (2 pixels higher)
PACKAGE_WAIT_FRAMES = 2  # The larger, the slower

# Package Y coordinates on conveyor belt
# conveyor0 = 83 (index 4) - RIGHT side (x > 229)
# conveyor1 = 83 (index 4) - LEFT side (83 <= x <= 204)
# conveyor2 = 72 (index 3)
# conveyor3 = 61 (index 2)
# conveyor4 = 50 (index 1)
# conveyor5 = 39 (index 0)

# X coordinates according to conveyor belt
# conveyor 0 -> x > 229 (right side, before Mario)
# conveyor 1 -> 83 <= x <= 204 (left side, after Mario)
# conveyor 2 and 4 -> 80 < X < 201
# conveyor 3 and 5 -> 83 < X < 204

# POSITIONS PACKAGES AT TRUCK (truck still)
# package 1 -> x = 36, y = 60
# package 2 -> x = 41, y = 60

TRUCK_PACKAGE_POSITIONS = [
    (36, 58),  # Package 1 (index 0) - 2 pixels higher
    (41, 58),  # Package 2 (index 1) - 2 pixels higher
    (36, 54),  # Package 3 (index 2) - 2 pixels higher
    (41, 54),  # Package 4 (index 3) - 2 pixels higher
    (36, 50),  # Package 5 (index 4) - 2 pixels higher
    (41, 50),  # Package 6 (index 5) - 2 pixels higher
    (36, 46),  # Package 7 (index 6) - 2 pixels higher
    (41, 46)   # Package 8 (index 7) - 2 pixels higher
]

# ---------------------------------
# TRUCK (18 high x 24 wide - extended 2 pixels to the right)
TRUCK_START = (24, 52)
TRUCK_SPRITE = (0, 0, 40, 24, 18)

# ---------------------------------
# BOSS
MARIO_FAIL = (249, 60)
LUIGI_FAIL = (26, 83)
BOSS_SPRITE_1 = (0, 0, 64, 12, 16)  # Currently uses Mario's sprite
BOSS_SPRITE_2 = (0, 16, 64, 18, 16)  # Currently uses Mario's sprite

# ---------------------------------
# LIVE
LIVE_SPRITE = (0, 0, 0, 12, 7)
