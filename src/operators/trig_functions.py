from __future__ import annotations
from .arithmetic import const, exp_n
from .base_arithmetic import ArithmeticOpBase, _single_arg
from math import sin, cos, tan, asin, acos, atan
from ..utilities import number

class sine (_single_arg):
    """Returns sin(x)."""
    def f(self, x: number) -> number:
        return sin(x)
    
    def f_prime(self) -> ArithmeticOpBase:
        return cosine()

    def __str__(self) -> str:
        return 'sin(x)'

class cosine (_single_arg):
    """Returns cos(x)."""
    def f(self, x: number) -> number:
        return cos(x)

    def f_prime(self) -> ArithmeticOpBase:
        return const(-1) * sine()

    def __str__(self) -> str:
        return 'cos(x)'

class tangent (_single_arg):
    """Returns tan(x)."""
    def f(self, x: number) -> number:
        return tan(x)

    def f_prime(self) -> ArithmeticOpBase:
        return tangent() ** 2 + 1

    def __str__(self) -> str:
        return 'tan(x)'

class arcsine (_single_arg):
    """Returns sin^-1(x)."""
    def f(self, x: number) -> number:
        return asin(x)

    def f_prime(self) -> ArithmeticOpBase:
        return const(1) / (const(1) - exp_n(2)) ** 0.5

    def __str__(self) -> str:
        return 'asin(x)'
        
class arccosine (_single_arg):
    """Returns cos^-1(x)."""
    def f(self, x: number) -> number:
        return acos(x)

    def f_prime(self) -> ArithmeticOpBase:
        return const(-1) / (const(1) - exp_n(2)) ** 0.5

    def __str__(self) -> str:
        return 'acos(x)'

class arctangent (_single_arg):
    """Returns tan^-1(x)."""
    def f(self, x: number) -> number:
        return atan(x)

    def f_prime(self) -> ArithmeticOpBase:
        return const(1) / (const(1) + exp_n(2))

    def __str__(self) -> str:
        return 'atan(x)'
