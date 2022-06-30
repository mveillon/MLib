import math
from typing import Set

def _n_twos(n: int) -> int:
    """Returns how many times n can be divided by two - O(logn) time."""
    res = 0
    while not n & 1:
        n >>= 1
        res += 1
    return res

def _odd_facs(n: int) -> Set[int]:
    """Returns the factors of n, assuming its odd - O(sqrt(n)) time."""
    assert n & 1, "_odd_facs: n must be odd!"
    res = {1, n}
    for i in range(3, math.floor(math.sqrt(n)) + 1, 2):
        if not n % i:
            res.add(i)
            res.add(n // i)
    return res

def factors(n: int) -> Set[int]:
    """Returns a set of all factors of n >= 0.

    O(sqrt(n)) time

    Args:
    :   n (int) : the number to factorize

    Returns:
    :   facts (set) : a set of all integer factors
    """
    if n == 0: return set()
    if n < 0: return factors(-n)
    if n & 1: return _odd_facs(n)

    res = {1, 2, n >> 1, n}
    twos = _n_twos(n)
    odd_facs = _odd_facs(n >> twos)
    for fac in odd_facs:
        for exp in range(twos):
            new_fac = fac << exp
            res.add(new_fac)
            res.add(n // new_fac)
    return res

def slow_fac(n: int) -> Set[int]:
    """A slower factorization algorithm.

    O(sqrt(n)) time

    Args:
    :   n (int) : the number to factorize

    Returns:
    :   facts (set) : a set of all integer factors
    """
    if n == 0: return set()
    if n < 0: return slow_fac(-n)
    if n & 1: return _odd_facs(n)
  
    res = {1, 2, n >> 1, n}
    for i in range(3, math.floor(math.sqrt(n)) + 1):
        if not n % i:
            res.add(i)
            res.add(n // i)
    return res

def is_prime(n: int) -> bool:
    """Returns whether a number is prime.

    O(sqrt(n)) time

    Args:
    :   n (int) : the number to check

    Returns:
    :   prime (bool) : whether the number is prime
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True
