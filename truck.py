"""
Truck Class
Manages the delivery truck logic.
"""

import constants
import pyxel

class Truck:
    """Represents the delivery truck."""

    def __init__(self, x: int, y: int):
        """
        Initializes the Truck object.
        :param x: The initial x coordinate of the truck
        :param y: The initial y coordinate of the truck
        """
        self.x = x
        self.y = y
        self.sprite = constants.TRUCK_SPRITE
        self.packages_count = 0  # Counter for packages in the truck
        self.is_leaving = False  # If the truck is leaving
        self.initial_x = x  # Save initial position

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @x.setter
    def x(self, x: int):
        if not isinstance(x, int):
            raise TypeError(f"The x must be an integer, {type(x)} provided")
        # Allow negative values so the truck can leave the screen
        else:
            self.__x = x

    @y.setter
    def y(self, y: int):
        if not isinstance(y, int):
            raise TypeError(f"The y must be an integer, {type(y)} provided")
        elif y < 0:
            raise ValueError("The y must be a non-negative number")
        else:
            self.__y = y

    def add_package(self):
        """Adds a package to the truck."""
        self.packages_count += 1
        if self.packages_count >= 8:
            self.is_leaving = True

    def update(self):
        """Updates the truck state."""
        if self.is_leaving:
            self.x -= 2  # The truck moves to the left
            # If the truck leaves the screen, reset it
            if self.x < -30:
                self.x = self.initial_x
                self.packages_count = 0
                self.is_leaving = False

    def is_full(self):
        """Checks if the truck is full."""
        return self.packages_count >= 8

    def draw(self):
        """Draws the truck and its packages."""
        # Draw Truck
        pyxel.blt(self.x, self.y, *self.sprite)

        # Draw Packages in Truck
        truck_offset_x = self.x - constants.TRUCK_START[0]
        limit = min(self.packages_count, 8)
        for i in range(limit):
            base_x, base_y = constants.TRUCK_PACKAGE_POSITIONS[i]
            pyxel.blt(base_x + truck_offset_x, base_y, *constants.PACKAGE_SPRITE_3)
