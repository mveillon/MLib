import math
from .utilities import can_be_int
from .factors import factors
from .fractions import gcd
from .utilities import number
from typing import List

def rad(n: int) -> str:
    """Takes a radicand and simplifies it.

    Args:
    :   n (int) : the number before the radical sign

    Returns:
    :   simple (str) : the simplified radical
    """
    if can_be_int(math.sqrt(n)):
        return str(int(math.sqrt(n)))

    facs = list(filter(lambda f: f != 1 and f != n and not n % (f * f), 
                       factors(n)))

    if facs:
        big_fac = max(facs)
        return f'{big_fac}√{n // (big_fac * big_fac)}'
    else:
        return f'√{n}'
    
def frac(num: int, denom: int) -> str:
    """Takes a fraction and simplifies it.

    Args:
    :   num (int) : the numerator
    :   denom (int) : the denominator

    Returns:
    :   simple (str) : the simplified fraction
    """
    if denom == 1 or num == 0:
        return str(num)
    elif num == denom:
        return '1'
    best = gcd(num, denom)
    if denom != best:
        return f'{num // best} / {denom // best}'
    return str(num // best)

def sep_rad(r: str) -> List[str]:
    """Separates the radical and returns it as a list.

    Args:
    :   r (str) : a string with a radical

    Returns:
    :   sep (list) : a list with the form [constant, radicand]
    """
    if '√' in r:
        res = r.split('√')
        res[1] = '√' + res[1]
        return res
    else:
        raise ValueError('No radical provided to sep_rad')

def frac_to_float(frac: str) -> float:
    """Converts a string fraction to a float.

    Args:
    ;   frac (str) : a string fraction with a '/' character somewhere

    Returns:
    :   quo (float) : the fraction evaluated
    """
    if can_be_int(frac):
        return int(frac)

    nums = frac.replace(' ', '').split('/')
    if nums[1]:
        return int(nums[0]) / int(nums[1])
    return int(nums[0])

def rad_to_float(rad_arg: str) -> float:
    """Converts a string version of a radical into a float.

    Args:
    :   rad_arg (str) : the string version of the radical with a '√' character somewhere

    Returns:
    :   root (float) : the evaluated radical
    """
    if can_be_int(rad_arg):
        return int(rad_arg)
    
    nums = rad_arg.replace(' ', '').split('√')
    if nums[0] and '/' in nums[0]:
        return frac_to_float(nums[0]) / math.sqrt(int(nums[1]))
    elif nums[0]:
        return int(nums[0]) * math.sqrt(int(nums[1]))
    return math.sqrt(int(nums[1]))
