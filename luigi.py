"""
Luigi
Subclass of Character
"""

from character import Character
import constants

class Luigi(Character):
    def __init__(self, x: int, y: int):
        """
        Constructor method for Luigi.
        Calls the parent class constructor (Character) and assigns the specific Luigi sprite.
        """
        # Call the __init__ of the parent class (Character)
        super().__init__(x, y)

        # Assign the sprite as an ATTRIBUTE
        self.sprite = constants.LUIGI_SPRITE

        # Save allowed Y positions
        self.y_positions = constants.LUIGI_Y_POSITIONS
        
        # Save the index of the current Y position
        try:
            self.current_y_index = self.y_positions.index(y)
        except ValueError:
            # If the initial Y is not in the list, assign the first one
            self.current_y_index = 0
            self.y = self.y_positions[0]

    def move_vertical(self, direction: str):
        """Moves Luigi vertically between predefined Y positions."""

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
