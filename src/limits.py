from copy import deepcopy
import math
from .frange import frange
from .utilities import close_enough

def analytical_limit(func, approaching, precision = 2, step = 1e-3):
    """Finds the analytical limit of the function approaching the given number.

    Args:
    :   func (function: float -> float) : the functiont to evaluation
    :   approaching (int | float) : the number to evaluate the limit at
    :   precision (int | float) : how many input values to test
    :   step (float) : how different the input values should be

    Returns:
    :   limit (float) : the analytical limit of the function
    """
    total_y = 0
    total_w = 0
    for i in frange(approaching - step * precision, approaching + step * (precision + 1), step):
        if not close_enough(i, approaching):
            w = step / math.fabs(approaching - i)
            total_y += func(i) * w
            total_w += w
    return total_y / total_w

def limit(func, approaching, precision = 2, step = 1e-3):
    """Returns the limit of the function at approaching.
    
    First checks if approaching is in the function's domain, then 
    finds the analytical limit

    Args:
    :   func (function: float -> float) : the functiont to evaluation
    :   approaching (int | float) : the number to evaluate the limit at
    :   precision (int | float) : how many input values to test
    :   step (float) : how different the input values should be

    Returns:
    :   limit (float) : the limit of the function
    """
    try:
        return func(approaching)
    except:
        return analytical_limit(func, approaching, precision, step)

def diff_quo(func, x):
    """Returns the derivative of func at x using the difference quotient.

    Args:
    :   func (function: float -> float) : the function to evaluate
    :   x (int | float) : the value to evaluate the function at

    Returns:
    :   quo (float) : the difference quotient of the function at x
    """
    return analytical_limit(lambda h: (func(x + h) - func(x)) / h, 0)

def assign_return(lst, ind, new_val):
    """Assigns new_val to lst[ind] and returns the list.

    Useful for lambda functions -
    Does not modify the original list

    Args:
    :   lst (list) : the list to change
    :   ind (int) : where to change the list
    :   new_val (any) : what to change the value to

    Returns:
    :   new_list (list) : the changed list
    """
    res = deepcopy(lst)
    res[ind] = new_val
    return res

def part_derivative(func, xs, x_ind):
    """Returns the partial derivative with respect to x_{x_ind} of xs.

    Args:
    ;   func (function: (listof float) -> float) : the function to evaluate
    :   xs (list) : the coordinate to evaluate the function at
    :   x_ind (int) : with which x value to evaluate the derivative with respect to

    Returns:
    :   part (float) : the partial derivative of the function at xs
    """
    return diff_quo(lambda n: func(assign_return(xs, x_ind, n)), xs[x_ind])

def get_root(func, guess, thresh = 1e-3, max_iters = 20):
    """Returns an approximation of the root (where it equals zero) of the function.

    Needs a reasonably good initial guess to work

    Args:
    :   func (float -> float) : the function to find the roots of
    :   guess (float) : the starting point
            needs to be reasonably good
    :   thresh (float) : how exact the estimate should be
    :   max_iters (int) : the maximum number of iterations to use

    Returns:
    :   root (float) : where the function equals zero
    """
    get_new = lambda g: guess - func(guess) / diff_quo(func, guess)
    new = get_new(guess)
    iters = 0
    while abs(new - guess) > thresh and iters < max_iters:
        guess = new
        new = get_new(guess)
        iters += 1
    return new

# def critical_points(func, n_xs, range_iter = frange(-20, 20, 5)):
#     roots = []
#     for xind in range(n_xs):
#         row = set()
#         for guess in range_iter:
#             row |= {round(get_root(lambda n: part_derivative(func, ), guess), 3)}
#         roots.append(row)
#     comped = roots[0]
#     for row in range(1, len(roots)):
#         comped &= row
#     return comped

# class _roundNode:
#     def __init__(self, data, ind):
#         self.data = data
#         self.ind = ind
    
#     def __eq__(self, other):
#         return self.data == other.data
