from typing import Any, Callable
from ..utilities import number

compare_callable = Callable[[number], bool]

def lt_n(n: number) -> compare_callable:
    """Returns a function that compares the input to n.
    
    Args:
    :   n (number) : the number to compare the input to

    Returns:
    :   comper (function (number -> number)) : a function that returns True iff the input is less than n    
    """
    return lambda x: x < n

def le_n(n: number) -> compare_callable:
    """Returns a function that compares the input to n.
    
    Args:
    :   n (number) : the number to compare the input to

    Returns:
    :   comper (function (number -> number)) : a function that returns True iff the input is less than or equal to n    
    """
    return lambda x: x <= n

def gt_n(n: number) -> compare_callable:
    """Returns a function that compares the input to n.
    
    Args:
    :   n (number) : the number to compare the input to

    Returns:
    :   comper (function (number -> number)) : a function that returns True iff the input is greater than n    
    """
    return lambda x: x > n

def ge_n(n: number) -> compare_callable:
    """Returns a function that compares the input to n.
    
    Args:
    :   n (number) : the number to compare the input to

    Returns:
    :   comper (function (number -> number)) : a function that returns True iff the input is greater than or equal to n    
    """
    return lambda x: x >= n

def invert() -> Callable[[Any], bool]:
    """Returns a function that returns the inverse of the input i.e. not x
    
    Args:
        None

    Returns:
    :   inverter (function (any -> bool)) : a function that returns the boolean inverse of the input
    """
    return lambda x: not x