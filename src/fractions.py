from __future__ import annotations
import numpy as np
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .utilities import number

class Fraction:
    """An alternative way of storing (rational) floating-point numbers.
    
    Stores them as a numerator-denominator pair. If num divides den, the
    constructor will return the integer quotient.

    Args:
        num (int) : the numerator

        den (int) : the denominator
    """
    def __init__(self, num: int, den: int):
        self._num: int = num
        self._den: int = den
        self._reduce()

    def __new__(cls, num, den):
        if num % den == 0:
            return num // den
        return super().__new__(cls)

    def __add__(first: Fraction, second: number) -> number:
        """Adds the two numbers or fractions and returns the result.

        Args:
        :   first (Fraction) : the first fraction
        :   second (Fraction | int | float) : the second number

        Returns:
        :   third (Fraction | int | float) : the sum of the two
        """
        if isinstance(second, Fraction):
            prod = lcm(first._den, second._den)
            num = ((prod * first._num // first._den) +
                   (prod * second._num // second._den))
            return Fraction(num, prod)
        if isinstance(second, int):
            return Fraction(first._num + second * first._den, first._den)
        if isinstance(second, float):
            return float(first) + second
        raise ValueError(f'Unsupported argument to Fraction operation: {second}')

    __radd__ = __add__

    def __sub__(first: Fraction, second: number) -> number:
        """Subtracts the second from the first.

        Args:
        :   first (Fraction) : the first fraction
        :   second (Fraction | int | float) : the second number

        Returns:
        :   third (Fraction | int | float) : the difference of the two
        """
        if isinstance(second, Fraction):
            return first + Fraction(-second._num, second._den)
        if isinstance(second, int) or isinstance(second, float):
            return first + -second
        raise ValueError(f'Unsupported argument to Fraction operation: {second}')

    def __rsub__(frac: Fraction, first: number) -> number:
        """Subtracts the fraction from first.
        
        Args:
        :   frac (Fraction) : the Fraction on the right side
        :   first (Fraction | int | float) : the number on the left side

        Returns:
        :   third (Fraction | int | float) : the difference of the two
        """
        return first + Fraction(-frac._num, frac._den)

    def __mul__(first: Fraction, second: number) -> number:
        """Returns the product of the two numbers.

        Args:
        :   first (Fraction) : the first fraction
        :   second (Fraction | int | float) : the second number

        Returns:
        :   third (Fraction | int | float) : the product of the two
        """
        if isinstance(second, Fraction):
            return Fraction(first._num * second._num,
                            first._den * second._den)
        if isinstance(second, int):
            return Fraction(first._num * second, first._den)
        if isinstance(second, float):
            return float(first) * second
        raise ValueError(f'Unsupported argument to Fraction operation: {second}')

    __rmul__ = __mul__

    def __str__(self) -> str:
        """A string representation of the fraction."""
        strs = [str(self._num), str(self._den)]
        lens = list(map(len, strs))
        big_ind = np.argmax(lens)
        sml_ind = 1 - big_ind
        l_spaces = (lens[big_ind] - lens[sml_ind]) // 2
        r_spaces = lens[big_ind] - lens[sml_ind] - l_spaces
        strs[sml_ind] = ''.join([' ' * l_spaces, strs[sml_ind], ' ' * r_spaces])
        return '\n'.join([strs[0], '-' * lens[big_ind], strs[1]])

    def __truediv__(first: Fraction, second: number) -> number:
        """Divides the first by the second.

        Args:
        :   first (Fraction) : the first fraction
        :   second (Fraction | int | float) : the second number

        Returns:
        :   third (Fraction | float) : the quotient of the two
        """
        if isinstance(second, Fraction):
            return first * Fraction(second._den, second._num)
        if isinstance(second, int):
            return Fraction(first._num, first._den * second)
        if isinstance(second, float):
            return float(first) / second
        raise ValueError(f'Unsupported argument to Fraction operation: {second}')

    def __rtruediv__(frac: Fraction, first: number) -> number:
        """Divides first by frac.
        
        Args:
        :   frac (Fraction) : the Fraction on the right side
        :   first (Fraction | int | float) : the number on the left side

        Returns:
        :   third (Fraction | float) : the quotient of the two
        """
        return first * Fraction(frac._den, frac._num)

    def __rpow__(frac: Fraction, base: number) -> number:
        """Raises base to the power of frac.
        
        Args:
        :   frac (Fraction) : the Fraction acting as the exponent
        :   base (Fraction | int | float) : the base of the expression

        Returns:
        :   third (Fraction | int | float) : base raised to frac
        """
        return base ** float(frac)

    def __pow__(frac: Fraction, power: number) -> number:
        """Raises frac the power of pow.
        
        Args:
        :   frac (Fraction) : the Fraction acting as the base
        :   power (Fraction | int | float) : the exponent of the expression

        Returns:
        :   third (Fraction | float) : frac raised to power
        """
        if isinstance(power, int):
            return Fraction(frac._num ** power, frac._den ** power)
        if isinstance(power, Fraction) or isinstance(power, float):
            return float(frac) ** float(power)
        raise ValueError(f'Unsupported argument to Fraction operation: {power}')

    def __int__(self) -> int:
        """Divides the numerator by the denominator, rounding down."""
        return self._num // self._den

    def __float__(self) -> float:
        """Divides the numberator by the denominator and provides a more exact value."""
        return self._num / self._den

    def _reduce(self) -> None:
        """Simplifies the fraction"""
        q = gcd(self._num, self._den)
        self._num //= q
        self._den //= q

    def __eq__(first, second) -> bool:
        """Returns whether the two fractions are equal."""
        if isinstance(second, Fraction):
            return first._num == second._num and first._den == second._den
        if isinstance(second, float):
            return float(first) == second
        if isinstance(second, int):
            return False
        raise ValueError(f'Unsupported argument to Fraction comparison: {second}')

    def __lt__(first, second) -> bool:
        """Returns whether the first is less than the second."""
        return float(first) < float(second)

    def __le__(first, second) -> bool:
        """Returns whether the first is less than or equal to the second."""
        return first < second or first == second

    def __gt__(first, second) -> bool:
        """Returns whether the first is greater than the second."""
        return not first <= second

    def __ge__(first, second) -> bool:
        """Returns whether the first is greater than or equal to the second."""
        return not first < second

    def reciprocal(self) -> number:
        """Returns the reciprocal of the fraction i.e. 1 / self.
        
        Args:
        :   None

        Returns:
        :   recip (Fraction) : the reciprocal
        """
        return Fraction(self._num, self._den)

    def __neg__(self) -> Fraction:
        """Returns -1 * self.
        
        Args:
        :   None

        Returns:
        :   negated (Fraction) : the negation of self
        """
        return Fraction(-self._num, self._den)

    def __floordiv__(first: Fraction, second: number) -> number:
        """Floor divides first by second.
        
        Args:
        :   first (Fraction) : the numerator
        :   second (Fraction | int | float) : the denominator

        Returns:
        :   third (int) : the floor division
        """
        return float(first) // second

    def __rfloordiv__(frac: Fraction, numerator: number) -> number:
        """Floor divides first by second.
        
        Args:
        :   frac (Fraction) : the numerator
        :   numberator (Fraction | int | float) : the denominator

        Returns:
        :   third (int) : the floor division
        """
        return numerator // float(frac)

def gcd(x: int, y: int) -> int:
    """Returns the greatest common denominator between x and y.

    O(log(min(x, y))) time.

    Args:
    :   x (int) : the first number
    :   y (int) : the second number

    Args:
    :   gcd (int) : the greatest number that divides both x and y
    """
    if x > y: return gcd(y, x)
    while y:
        x, y = y, x % y
    return x

def lcm(x: int, y: int) -> int:
    """Returns the least common multiple of x and y.

    uses the fact that x * y == lcm * gcd.

    O(log(min(x, y))) time.

    Args:
    :   x (int) : the first number
    :   y (int) : the second number

    Returns:
    :   lcm (int) : the smallest number that both x and y are factors of
    """
    return (x * y) // gcd(x, y)

def divide(num: int, den: int) -> number:
    """Divides num by den, returning an exact Fraction if they do not divide.

    Note that, because the Fraction constructor simplifies itself and can return
    an integer, this function ends up being just an alias for the Fraction constructor.
    
    Args:
    :   num (int) : the numerator
    :   den (int) : the denominator

    Returns:
    :   q (int | Fraction) : the quotient of the two
    """
    return Fraction(num, den)

def frac_abs(n: number) -> number:
    """Returns the absolute value of any number, incuding Fractions.
    
    Args:
    :   n (int | float | Fraction) : the number to find the absolute value of

    Returns:
    :   abs (int | float | Fraction) : the absolute value
    """
    return -n if n < 0 else n
