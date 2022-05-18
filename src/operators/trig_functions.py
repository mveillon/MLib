from .arithmetic import const, exp_n
from .base_arithmetic import _single_arg
from math import sin, cos, tan, asin, acos, atan

class sine (_single_arg):
    """Returns sin(x)."""
    def f(self, x):
        return sin(x)
    
    def f_prime(self):
        return cosine()

    def __str__(self):
        return 'sin(x)'

class cosine (_single_arg):
    """Returns cos(x)."""
    def f(self, x):
        return cos(x)

    def f_prime(self):
        return const(-1) * sine()

    def __str__(self):
        return 'cos(x)'

class tangent (_single_arg):
    """Returns tan(x)."""
    def f(self, x):
        return tan(x)

    def f_prime(self):
        return tangent() ** 2 + 1

    def __str__(self):
        return 'tan(x)'

class arcsine (_single_arg):
    """Returns sin^-1(x)."""
    def f(self, x):
        return asin(x)

    def f_prime(self):
        return const(1) / (const(1) - exp_n(2)) ** 0.5

    def __str__(self):
        return 'asin(x)'
        
class arccosine (_single_arg):
    """Returns cos^-1(x)."""
    def f(self, x):
        return acos(x)

    def f_prime(self):
        return const(-1) / (const(1) - exp_n(2)) ** 0.5

    def __str__(self):
        return 'acos(x)'

class arctangent (_single_arg):
    """Returns tan^-1(x)."""
    def f(self, x):
        return atan(x)

    def f_prime(self):
        return const(1) / (const(1) + exp_n(2))

    def __str__(self):
        return 'atan(x)'
