"""
Bachelor in Data Science and Engineering 
Subject: Programming
Created by Camila Alba Agresta Kohen  
Created on 11/11/25 at 11:40
Universidad Carlos III de Madrid
Student

-------
Final project
Super Mario
"""

class Package:
    """ A Package class where we need only direction and at_truck to give initial
    values for the attributes """
    def __init__(self, direction:str, at_truck: bool):
        self.level = 0
        self.position = 0
        self.direction = direction
        self.at_truck = at_truck
        if self.direction == "right":
            self.image = "Package_Right.png"
        else:
            self.image = "Package_Left.png"

    @property
    def direction(self) -> str:
        return self.__direction

    @direction.setter
    def direction(self, direction: str):
        if not isinstance(direction, str):
            raise TypeError("The direction must be a string")
        # elif direction.lower() not in ("left", "right")
        else:
            direction_names = ("left", "right")
            if direction.lower() not in direction_names:
                raise ValueError (direction + " is not a valid direction name. Valid ones are" +
                                  str(direction_names))
            else:
                self.__direction = direction.lower()
