from typing import Union, Any
from .fractions import Fraction

number = Union[int, float, Fraction]

def even(n: int) -> bool:
    """Returns whether n is even."""
    return not n & 1

def odd(n: int) -> bool:
    """Returns whether n is odd."""
    return bool(n & 1)

def is_truthy(thing: Any) -> bool:
    """Returns whether thing is truthy."""
    return bool(thing)
    
def close_enough(num1: number, num2: number) -> bool:
    """Returns whether the two numbers are close enough within floating point error."""
    diff = num1 - num2
    return diff < 0.001 and diff > -0.001

def can_be_int(thing: Any) -> bool:
    """Returns whether thing can be an integer.

    If thing is a float, it will check if thing is close_enough to the nearest integer.
    Otherwise it will try to cast thing as an int

    Args:
    :   thing (any) : the object to look at

    Returns:
    :   is_int (bool) : whether the object can be an int
    """
    if type(thing) == float:
        return close_enough(thing, round(thing))
    try:
        n = int(thing)
        return True
    except ValueError:
        return False
