"""
Boss Class
The boss who scolds Mario and Luigi when a package falls.
"""

import constants

class Boss:
    """Represents the boss character."""

    def __init__(self, x: int, y: int):
        """
        Initializes the Boss object.
        :param x: The initial x coordinate of the boss
        :param y: The initial y coordinate of the boss
        """
        self.x = x
        self.y = y
        self.sprite = constants.BOSS_SPRITE_1
        self.animation_frame = 0
        self.is_visible = False  # The boss only appears when a package falls
        self.flipped = False  # If True, the sprite is flipped horizontally

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @property
    def is_visible(self) -> bool:
        return self.__is_visible

    @x.setter
    def x(self, x: int):
        if not isinstance(x, int):
            raise TypeError(f"The x must be an integer, {type(x)} provided")
        elif x < 0:
            raise ValueError("The x must be a non-negative number")
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

    @is_visible.setter
    def is_visible(self, visible: bool):
        if not isinstance(visible, bool):
            raise TypeError("The is_visible must be a boolean")
        else:
            self.__is_visible = visible

    def show(self):
        """Shows the boss on the screen."""
        self.is_visible = True

    def hide(self):
        """Hides the boss from the screen."""
        self.is_visible = False

    def animate(self):
        """Alternates between the two boss sprites to create animation."""
        self.animation_frame += 1
        if self.animation_frame % 10 == 0:  # Change every 10 frames
            if self.sprite == constants.BOSS_SPRITE_1:
                self.sprite = constants.BOSS_SPRITE_2
            else:
                self.sprite = constants.BOSS_SPRITE_1
