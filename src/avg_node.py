from __future__ import annotations
from typing import Union
from .utilities import number
from .fractions import Fraction

class Avg_Node:
    """An easy and efficient way to find the average of something.

    O(1) space

    Args:
        None
    """
    def __init__(self):
        self.count: int = 0
        self.data: number = 0

    def __add__(self, num: Union[int, float]) -> Avg_Node:
        """Adds the number to the average and adds one to the total count.

        Faster than just adding num / total_count because this doesn't
        require a division per addition. 
        O(1) time

        Args:
        :   num (int | float) : the number to add

        Returns:
        :   self
        """
        self.count += 1
        self.data += num
        return self

    def avg(self) -> number:
        """Returns the compiled average.

        O(1) time

        Args:
        :   None
        
        Returns:
        :   avg (float) : the average
        """
        if self.count:
            return self.data / self.count
        else:
            return 0

    def __str__(self) -> str:
        """A string representation of the average."""
        a = self.avg()
        if isinstance(a, Fraction):
            return str(a)
        return str(round(a, 3))
    