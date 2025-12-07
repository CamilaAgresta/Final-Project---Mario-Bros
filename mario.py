"""
Mario
Subclass of Character
"""
from character import Character
import constants

class Mario(Character):
    def __init__(self, x: int, y: int):
        """
        Constructor method for Mario.
        Calls the parent class constructor (Character) and assigns the specific Mario sprite.
        """
        # Call the __init__ of the parent class (Character)
        super().__init__(x, y)

        # Assign the sprite as an ATTRIBUTE
        # The tuple is (bank_img, x_in_bank, y_in_bank, width, height)
        self.sprite = constants.MARIO_SPRITE
        self.sprite_flip = constants.MARIO_SPRITE_FLIP

        # Save allowed Y positions
        self.y_positions = constants.MARIO_Y_POSITIONS
        
        # Save the index of the current Y position
        # (Since MARIO_START is (215, 83), and 83 is the last in the tuple, the initial index will be 2)
        try:
            self.current_y_index = self.y_positions.index(y)
        except ValueError:
            # If the initial Y is not in the list, assign the first one
            self.current_y_index = 0
            self.y = self.y_positions[0]

    def move_vertical(self, direction: str):
        """Moves Mario vertically between predefined Y positions."""

        if direction.lower() == 'up':
            # Move to a smaller Y (higher on the screen)
            # If the current index is > 0, can move up
            if self.current_y_index > 0:
                self.current_y_index -= 1
                self.y = self.y_positions[self.current_y_index]

        elif direction.lower() == 'down':
            # Move to a larger Y (lower on the screen)
            # If the current index is less than the last index (length - 1), can move down
            if self.current_y_index < len(self.y_positions) - 1:
                self.current_y_index += 1
                self.y = self.y_positions[self.current_y_index]

    def flipped(self):
        if self.y in (constants.MARIO_Y_POSITIONS[0], constants.MARIO_Y_POSITIONS[1]):
            # Mario in the secon or third position
            self.sprite = self.sprite_flip
        else:
            # first position  → normal sprite
            self.sprite = constants.MARIO_SPRITE

    def draw(self):
        """Draws Mario, checking flip state first."""
        self.flipped()
        super().draw()



