from __future__ import annotations
from typing import Tuple, Any
from ..utilities import number

from .arithmetic import mult_n, const, identity, log_base_n
from .base_arithmetic import ArithmeticOpBase, simple_return, operator_input
from math import e

class TwoFunctionsBase (ArithmeticOpBase):
    """Abstract base class for functions that combine two functions.
    
    Args:
        first (ArithmeticOpBase) : an object derived from ArithmeticOpBase which
            acts as the first function
        second (ArithmeticOpBase) : an object derived from ArithmeticOpBase which 
            acts as the second function
    """
    def __init__(self, first: ArithmeticOpBase, second: ArithmeticOpBase):
        self.first = first
        self.second = second

    def __new__(cls, f, g):
        o = object.__new__(cls)
        o.__init__(f, g)
        return o

    def _fg_str(self) -> Tuple[str, str]:
        """Returns how f and g should be represented as strings, with parenthesis and such."""
        res = []
        for func in [self.first, self.second]:
            f_str = str(func)
            res.append(f'({f_str})' if func.priority < self.priority else f_str)
        return res[0], res[1]

class chain (TwoFunctionsBase):
    """Returns first(second(x)), with arbitrary functions first and second."""
    def __init__(self, first: ArithmeticOpBase, second: ArithmeticOpBase):
        super().__init__(first, second)
        self.priority = 5

    def f(self, x: number) -> number:
        return self.first(self.second(x))

    def f_prime(self) -> ArithmeticOpBase:
        return chain(self.first.f_prime(), self.second) * self.second.f_prime()

    def __str__(self) -> str:
        return str(self.first).replace('x', str(self.second))

    def __new__(cls, f, g):
        if _isnum(f):
            return f
        if _isnum(g):
            return const(f(g.n))
        if isinstance(f, identity):
            return g
        return super(chain, cls).__new__(cls, f, g)

class f_plus_g (TwoFunctionsBase):
    """Returns first(x) + second(x)."""
    def __init__(self, first: ArithmeticOpBase, second: ArithmeticOpBase):
        super().__init__(first, second)
        self.priority = 0

    def f(self, x: number) -> number:
        return self.first(x) + self.second(x)

    def f_prime(self) -> ArithmeticOpBase:
        return self.first.f_prime() + self.second.f_prime()

    def __str__(self) -> str:
        f_str, g_str = self._fg_str()
        return f'{f_str} + {g_str}'

    def __new__(cls, f, g):
        s = f._simple_add(g)
        return super(f_plus_g, cls).__new__(cls, f, g) if s is None else s

class f_minus_g (TwoFunctionsBase):
    """Returns first(x) - second(x)."""
    def __init__(self, first: ArithmeticOpBase, second: ArithmeticOpBase):
        super().__init__(first, second)
        self.priority = 1

    def f(self, x: number) -> number:
        return self.first(x) - self.second(x)

    def f_prime(self) -> ArithmeticOpBase:
        return self.first.f_prime() - self.second.f_prime()

    def __str__(self) -> str:
        f_str, g_str = self._fg_str()
        return f'{f_str} - {g_str}'

    def __new__(cls, f, g):
        s = f._simple_sub(g)
        return super(f_minus_g, cls).__new__(cls, f, g) if s is None else s

class f_times_g (TwoFunctionsBase):
    """Returns first(x) * second(x)."""
    def __init__(self, first: ArithmeticOpBase, second: ArithmeticOpBase):
        super().__init__(first, second)
        self.priority = 2

    def f(self, x: number) -> number:
        return self.first(x) * self.second(x)

    def f_prime(self) -> ArithmeticOpBase:
        return self.first.f_prime() * self.second + self.first * self.second.f_prime()

    def __str__(self) -> str:
        both = [self.first, self.second]
        for i in range(len(both)):
            if _isnum(both[i]):
                if both[i].n == 1:
                    return str(both[1 - i])
                if both[i].n == -1:
                    return f'-({str(both[1 - i])})'
                return f'{both[i].n}({str(both[1 - i])})'
        
        f_str, g_str = self._fg_str()
        return f'{f_str} * {g_str}'

    def __new__(cls, f, g):
        s = f._simple_mul(g)
        return super(f_times_g, cls).__new__(cls, f, g) if s is None else s

class f_divided_by_g (TwoFunctionsBase):
    """Returns first(x) / second(x)."""
    def __init__(self, first: ArithmeticOpBase, second: ArithmeticOpBase):
        super().__init__(first, second)
        self.priority = 3

    def f(self, x: number) -> number:
        return self.first(x) / self.second(x)

    def f_prime(self) -> ArithmeticOpBase:
        # TODO : why can't we change the denominator to self.second ** 2?
        return ((self.first.f_prime() * self.second - self.first * self.second.f_prime()) /
                (self.second * self.second))
                              
    def __str__(self) -> str:
        f_str, g_str = self._fg_str()
        return f'{f_str} / {g_str}'

    def __new__(cls, f, g):
        s = f._simple_div(g)
        return super(f_divided_by_g, cls).__new__(cls, f, g) if s is None else s

class f_raised_to_g (TwoFunctionsBase):
    """Returns first(x) ** second(x)."""
    def __init__(self, first: ArithmeticOpBase, second: ArithmeticOpBase):
        super().__init__(first, second)
        self.priority = 4

    def f(self, x: number) -> number:
        return self.first(x) ** self.second(x)

    def f_prime(self) -> ArithmeticOpBase:
        fx = self.first
        fpx = self.first.f_prime()
        gx = self.second
        gpx = self.second.f_prime()
        return fx ** gx * (gpx * chain(log_base_n(e), fx) + gx * (fpx / fx))

    def __str__(self) -> str:
        f_str, g_str = self._fg_str()
        return f'{f_str} ^ {g_str}'

    def __new__(cls, f, g):
        if isinstance(f, const) and isinstance(g, log_base_n) and f.n == g.n:
            return identity()
        s = f._simple_exp(g)
        return super(f_raised_to_g, cls).__new__(cls, f, g) if s is None else s

def _isnum(func: Any) -> bool:
    """Returns whether func is a constant number."""
    return isinstance(func, const)

def mx_plus_b(m: number, b: number) -> ArithmeticOpBase:
    """Returns a function of the form y = mx + b.
    
    Args:
    :   m (number) : the slope of the line
    :   b (number) : the y-intercept of the line

    Returns:
    :   f (ArithmeticOpBase) : an object that acts like the noted function,
            but with a derivative as well
    """
    return mult_n(m) + b
