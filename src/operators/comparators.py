def lt_n(n):
    """Returns a function that compares the input to n.
    
    Args:
    :   n (number) : the number to compare the input to

    Returns:
    :   comper (function (number -> number)) : a function that returns True iff the input is less than n    
    """
    return lambda x: x < n

def le_n(n):
    """Returns a function that compares the input to n.
    
    Args:
    :   n (number) : the number to compare the input to

    Returns:
    :   comper (function (number -> number)) : a function that returns True iff the input is less than or equal to n    
    """
    return lambda x: x <= n

def gt_n(n):
    """Returns a function that compares the input to n.
    
    Args:
    :   n (number) : the number to compare the input to

    Returns:
    :   comper (function (number -> number)) : a function that returns True iff the input is greater than n    
    """
    return lambda x: x > n

def ge_n(n):
    """Returns a function that compares the input to n.
    
    Args:
    :   n (number) : the number to compare the input to

    Returns:
    :   comper (function (number -> number)) : a function that returns True iff the input is greater than or equal to n    
    """
    return lambda x: x >= n

def invert():
    """Returns a function that returns the inverse of the input i.e. not x
    
    Args:
        None

    Returns:
    :   inverter (function (any -> bool)) : a function that returns the boolean inverse of the input
    """
    return lambda x: not x