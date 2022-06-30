from typing import List, Any, Callable

def get_n(n: int) -> Callable[[List[Any]], Any]:
    """Returns a function that returns the nth element of a collection.
    
    Args:
    :   n (int) : the number to use as the index

    Returns:
    :   getter (function (collection -> any)) : a function that returns collection[n]
    """
    return lambda coll: coll[n]

def set_n_to_val(n: int, val: Any) -> Callable[[List[Any]], None]:
    """Returns a function that sets the nth element of a collection to val.
    
    Args:
    :   n (int) : the number to use as the index
    :   val (any) : what to set the value of the collection to

    Returns:
    :   setter (function (collection -> void)) : a function that sets collection[n] to val
    """
    def setter(coll):
        coll[n] = val
    return setter
