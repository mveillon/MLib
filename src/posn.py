import math
from .utilities import can_be_int
from .string_math import rad

class Posn:
    """A container for 2D positions that supports lots of operations.

    Args:
        x (int | float) : the x coordinate
        
        y (int | float) : the y coordinate
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __str__(self):
        """A string representation of the position."""
        return f'({self.x}, {self.y})'
    
    def __eq__(self, other):
        """Returns whether the two positions are equal."""
        return self.x == other.x and self.y == other.y
    
    def __ne__(self, other):
        """Returns whether the two positions are not equal."""
        return not self == other
    
    def __gt__(self, other):
        """Returns whether the first posn is greater lexigraphically."""
        if self.x == other.x:
            return self.y > other.y
        else:
            return self.x > other.x
        
    def __lt__(self, other):
        """Returns whether the first posn is lesser lexigraphically."""
        return not (self > other or self == other)
    
    def __ge__(self, other):
        """Returns whether the first posn is greater or equal lexigraphically."""
        return self > other or self == other
    
    def __le__(self, other):
        """Returns whether the first posn is lesser or equal lexigraphically."""
        return self < other or self == other
    
    def distance(self, other):
        """Returns the distance between the positions as a string."""
        res = ((other.x - self.x) ** 2 +
               (other.y - self.y) ** 2)
        if can_be_int(math.sqrt(res)):
            return str(int(math.sqrt(res)))

        return rad(res)
  