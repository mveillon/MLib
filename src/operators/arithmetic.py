from __future__ import annotations
from math import log, e
import numpy as np
from ..fractions import Fraction
from .base_arithmetic import ArithmeticOpBase, _single_arg, operator_input, simple_return
from ..utilities import number

class const (ArithmeticOpBase):
    """Always returns n i.e. f(x) = n."""
    def __init__(self, n: number):
        super().__init__(n)
        self.priority = 6

    def f(self, x: number) -> number:
        return self.n

    def f_prime(self) -> ArithmeticOpBase:
        return const(0)

    def __str__(self) -> str:
        return str(self.n)

    def _simple_add(self, other: operator_input) -> simple_return:
        other = self._get_func(other)
        if self.n == 0:
            return other
        if isinstance(other, const):
            return const(self.n + other.n)
        if isinstance(other, add_n):
            return add_n(self.n + other.n)
        if isinstance(other, sub_n):
            return add_n(self.n - other.n)
        if isinstance(other, n_sub):
            return n_sub(self.n + other.n)
        if isinstance(other, identity):
            return add_n(self.n)
        return super()._simple_add(other)

    def _simple_sub(self, other: operator_input) -> simple_return:
        other = self._get_func(other)
        if self.n == 0:
            return other * -1
        if isinstance(other, const):
            return const(self.n - other.n)
        if isinstance(other, add_n):
            return n_sub(self.n - other.n)
        if isinstance(other, sub_n):
            return n_sub(self.n + other.n)
        if isinstance(other, n_sub):
            return add_n(self.n - other.n)
        if isinstance(other, identity):
            return n_sub(self.n)
        return super()._simple_sub(other)

    def _simple_mul(self, other: operator_input) -> simple_return:
        other = self._get_func(other)
        if self.n == 0:
            return const(0)
        if self.n == 1:
            return other
        if isinstance(other, const):
            return const(self.n * other.n)
        if isinstance(other, mult_n) or isinstance(other, n_div):
            return type(other)(self.n * other.n)
        if isinstance(other, identity):
            return mult_n(self.n)
        return super()._simple_mul(other)

    def _simple_div(self, other: operator_input) -> simple_return:
        other = self._get_func(other)
        if self.n == 0:
            return const(0)
        if isinstance(other, const):
            return const(self.n / other.n)
        if isinstance(other, div_n):
            return n_div(self.n * other.n)
        if isinstance(other, identity):
            return n_div(self.n)
        return super()._simple_div(other)

    def _simple_exp(self, other: operator_input) -> simple_return:
        other = self._get_func(other)
        if self.n == 0 or self.n == 1:
            return self
        if isinstance(other, const):
            return const(self.n ** other.n)
        return super()._simple_exp(other)

class identity (_single_arg):
    """Always returns x i.e. f(x) = x."""
    def __init__(self):
        self.priority = 6

    def f(self, x: number) -> number:
        return x

    def f_prime(self) -> ArithmeticOpBase:
        return const(1)

    def __str__(self) -> str:
        return 'x'

    def _simple_add(self, other: operator_input) -> simple_return:
        other = self._get_func(other)
        if isinstance(other, identity):
            return mult_n(2)
        return other + self

    def _simple_mul(self, other: operator_input) -> simple_return:
        other = self._get_func(other)
        if isinstance(other, identity):
            return exp_n(2)
        return other * self

    def _simple_sub(self, other: operator_input) -> simple_return:
        other = self._get_func(other)
        if isinstance(other, identity):
            return const(0)
        if isinstance(other, const):
            return const(-other.n) + self
        if isinstance(other, add_n):
            return const(-other.n)
        if isinstance(other, sub_n):
            return const(other.n)
        return super()._simple_sub(other)

    def _simple_div(self, other: operator_input) -> simple_return:
        other = self._get_func(other)
        if isinstance(other, identity):
            return const(1)
        if isinstance(other, const):
            return div_n(other.n)
        if isinstance(other, mult_n):
            return const(1 / other.n)
        if isinstance(other, div_n):
            return const(other.n)
        return super()._simple_div(other)

class add_n (ArithmeticOpBase):
    """Adds x to n i.e. f(x) = x + n."""
    def __init__(self, n: number):
        super().__init__(n)
        self.priority = 0

    def f(self, x: number) -> number:
        return self.n + x

    def f_prime(self) -> ArithmeticOpBase:
        return const(1)

    def __str__(self) -> str:
        return f'x + {self.n}'

    def __new__(cls, n):
        if n == 0:
            return identity()
        if n < 0:
            return sub_n(-n)
        return super(add_n, cls).__new__(cls, n)

    def _simple_add(self, other: operator_input) -> simple_return:
        other = self._get_func(other)
        if isinstance(other, const):
            return other + self
        if isinstance(other, add_n):
            return mult_n(2) + (self.n + other.n)
        if isinstance(other, sub_n):
            if self.n > other.n:
                return mult_n(2) + (self.n - other.n)
            return mult_n(2) - (other.n - self.n)
        if isinstance(other, n_sub):
            return const(self.n + other.n)
        if isinstance(other, identity):
            return mult_n(2) + const(self.n)
        return super()._simple_add(other)

    def _simple_sub(self, other: operator_input) -> simple_return:
        other = self._get_func(other)
        if isinstance(other, const):
            return add_n(self.n - other.n)
        if isinstance(other, add_n):
            return const(self.n - other.n)
        if isinstance(other, sub_n):
            return const(self.n + other.n)
        if isinstance(other, n_sub):
            return mult_n(2) + (self.n - other.n)
        if isinstance(other, identity):
            return const(self.n)
        return super()._simple_sub(other)

class sub_n (ArithmeticOpBase):
    """Subtracts n from x i.e. f(x) = x - n."""
    def __init__(self, n):
        super().__init__(n)
        self.priority = 1

    def f(self, x: number) -> number:
        return x - self.n

    def f_prime(self) -> ArithmeticOpBase:
        return const(1)

    def __str__(self) -> str:
        return f'x - {self.n}'

    def __new__(cls, n):
        if n == 0:
            return identity()
        if n < 0:
            return add_n(-n)
        return super(sub_n, cls).__new__(cls, n)

    def _simple_add(self, other: operator_input) -> simple_return:
        other = self._get_func(other)
        if isinstance(other, const) or isinstance(other, add_n):
            return other + self
        if isinstance(other, sub_n):
            return mult_n(2) - (self.n + other.n)
        if isinstance(other, n_sub):
            return const(other.n - self.n)
        if isinstance(other, identity):
            return mult_n(2) - self.n
        return super()._simple_add(other)

    def _simple_sub(self, other: operator_input) -> simple_return:
        other = self._get_func(other)
        if isinstance(other, const):
            return sub_n(self.n + other.n)
        if isinstance(other, add_n):
            return const(-self.n - other.n)
        if isinstance(other, sub_n):
            return const(other.n - self.n)
        if isinstance(other, n_sub):
            return mult_n(2) - (self.n + other.n)
        if isinstance(other, identity):
            return const(-self.n)
        return super()._simple_sub(other)

class n_sub (ArithmeticOpBase):
    """Subtracts x from n i.e. f(x) = n - x."""
    def __init__(self, n: number):
        super().__init__(n)
        self.priority = 1

    def f(self, x: number) -> number:
        return self.n - x

    def f_prime(self) -> ArithmeticOpBase:
        return const(-1)

    def __str__(self) -> str:
        return f'{self.n} - x'

    def __new__(cls, n):
        if n == 0:
            return mult_n(-1)
        return super(n_sub, cls).__new__(cls, n)

    def _simple_add(self, other: operator_input) -> simple_return:
        other = self._get_func(other)
        if isinstance(other, const) or isinstance(other, add_n) or isinstance(other, sub_n):
            return other + self
        if isinstance(other, n_sub):
            return mult_n(-2) + (self.n + other.n)
        if isinstance(other, identity):
            return const(self.n)
        return super()._simple_add(other)

    def _simple_sub(self, other: operator_input) -> simple_return:
        other = self._get_func(other)
        if isinstance(other, const):
            return n_sub(self.n - other.n)
        if isinstance(other, add_n):
            return mult_n(-2) + (self.n - other.n)
        if isinstance(other, sub_n):
            return mult_n(-2) + (self.n + other.n)
        if isinstance(other, n_sub):
            return const(self.n - other.n)
        if isinstance(other, identity):
            return mult_n(-2) + self.n
        return super()._simple_sub(other)

class mult_n (ArithmeticOpBase):
    """Multiplies n with the output i.e. f(x) = nx."""
    def __init__(self, n: number):
        super().__init__(n)
        self.priority = 2

    def f(self, x: number) -> number:
        return x * self.n

    def f_prime(self) -> ArithmeticOpBase:
        return const(self.n)

    def __str__(self) -> str:
        if self.n == 1:
            return 'x'
        if self.n == -1:
            return '(-x)'
        return f'{self.n}x'

    def __new__(cls, n):
        if n == 0:
            return const(0)
        if n == 1:
            return identity()
        return super(mult_n, cls).__new__(cls, n)

    def _simple_mul(self, other: operator_input) -> simple_return:
        other = self._get_func(other)
        if isinstance(other, const):
            return other * self
        if isinstance(other, mult_n):
            return exp_n(2) * (self.n * other.n)
        if isinstance(other, div_n):
            return exp_n(2) * (self.n / other.n)
        if isinstance(other, n_div):
            return const(self.n * other.n)
        if isinstance(other, identity):
            return exp_n(2) * self.n
        return super()._simple_mul(other)

    def _simple_div(self, other: operator_input) -> simple_return:
        other = self._get_func(other)
        if isinstance(other, const):
            return mult_n(self.n / other.n)
        if isinstance(other, mult_n):
            return const(self.n / other.n)
        if isinstance(other, div_n):
            return self * n_div(other.n)
        if isinstance(other, n_div):
            return self * div_n(other.n)
        if isinstance(other, identity):
            return const(self.n)
        return super()._simple_div(other)

class div_n (ArithmeticOpBase):
    """Divides x by n i.e. f(x) = x / n."""
    def __init__(self, n: number):
        super().__init__(n)
        self.priority = 3
        if self.n == 0:
            raise ZeroDivisionError('Cannot create div_n class with n = 0')
        self.recip = 1 / self.n

    def __new__(cls, n):
        if n == 1:
            return identity()
        return super(div_n, cls).__new__(cls, n)

    def f(self, x: number) -> number:
        return x / self.n

    def f_prime(self) -> ArithmeticOpBase:
        return const(self.recip)

    def __str__(self) -> str:
        return f'x / {self.n}'

    def _simple_mul(self, other: operator_input) -> simple_return:
        other = self._get_func(other)
        if isinstance(other, const):
            return other * self
        if isinstance(other, mult_n):
            return exp_n(2) * (other.n / self.n)
        if isinstance(other, div_n):
            return exp_n(2) / (self.n * other.n)
        if isinstance(other, n_div):
            return const(other.n / self.n)
        if isinstance(other, identity):
            return exp_n(2) / self.n
        return super()._simple_mul(other)
    
    def _simple_div(self, other: operator_input) -> simple_return:
        other = self._get_func(other)
        if isinstance(other, const) or isinstance(other, mult_n):
            return other * n_div(self.n)
        if isinstance(other, div_n):
            return self * n_div(other.n)
        if isinstance(other, n_div):
            return self * div_n(other.n)
        if isinstance(other, identity):
            return const(1 / self.n)
        return super()._simple_div(other)

class n_div (ArithmeticOpBase):
    """Divides n by x i.e. f(x) = n / x."""
    def __init__(self, n: number):
        super().__init__(n)
        self.priority = 3

    def f(self, x: number) -> number:
        return self.n / x

    def f_prime(self) -> ArithmeticOpBase:
        return const(-self.n) / exp_n(2)

    def __str__(self) -> str:
        return f'{self.n} / x'

    def __new__(cls, n):
        if n == 0:
            return const(0)
        return super(n_div, cls).__new__(cls, n)

    def _simple_mul(self, other: operator_input) -> simple_return:
        other = self._get_func(other)
        if isinstance(other, const) or isinstance(other, mult_n) or isinstance(other, div_n):
            return other * self
        if isinstance(other, n_div):
            return const(self.n * other.n) / exp_n(2)
        if isinstance(other, identity):
            return const(self.n)
        return super()._simple_mul(other)

    def _simple_div(self, other: operator_input) -> simple_return:
        other = self._get_func(other)
        if isinstance(other, const):
            return n_div(self.n / other.n)
        if isinstance(other, mult_n):
            return const(self.n / other.n) / exp_n(2)
        if isinstance(other, div_n):
            return self * n_div(other.n)
        if isinstance(other, n_div):
            return self * div_n(other.n)
        if isinstance(other, identity):
            return const(self.n) / exp_n(2)
        return super()._simple_div(other)

class floordiv_n (ArithmeticOpBase):
    """Floor divides x by n i.e. f(x) = x // n."""
    def __init__(self, n: number):
        super().__init__(n)
        self.priority = 3

    def f(self, x: number) -> number:
        return x // self.n

    def f_prime(self) -> ArithmeticOpBase:
        return const(0)

    def __str__(self) -> str:
        return f'x // {self.n}'

class n_floordiv (ArithmeticOpBase):
    """Floor divides x by n i.e. f(x) = n // x."""
    def __init__(self, n: number):
        super().__init__(n)
        self.priority = 3

    def f(self, x: number) -> number:
        return self.n // x

    def f_prime(self) -> ArithmeticOpBase:
        return const(0)

    def __str__(self) -> str:
        return f'{self.n} // x'

    def __new__(cls, n):
        if n == 0:
            return const(0)
        return super(n_floordiv, cls).__new__(cls, n)

class exp_n (ArithmeticOpBase):
    """Raises x to the power of n i.e. f(x) = x ** n."""
    def __init__(self, n: number):
        super().__init__(n)
        self.priority = 4

    def f(self, x: number) -> number:
        return x ** self.n

    def f_prime(self) -> ArithmeticOpBase:
        return exp_n(self.n - 1) * self.n

    def __str__(self):
        return f'x^{self.n}'

    def __new__(cls, n):
        if n == 0:
            return const(1)
        if n == 1:
            return identity()
        return super(exp_n, cls).__new__(cls, n)

    def _simple_mul(self, other: operator_input) -> simple_return:
        other = self._get_func(other)
        if isinstance(other, identity):
            return exp_n(self.n + 1)
        return super()._simple_mul(other)

class n_exp (ArithmeticOpBase):
    """Raises n to the power of x i.e. f(x) = n ** x."""
    def __init__(self, n: number):
        super().__init__(n)
        self.priority = 4
        self.ln = log(self.n) if self.n > 0 else None

    def f(self, x: number) -> number:
        return self.n ** x

    def f_prime(self) -> ArithmeticOpBase:
        if self.ln is None:
            raise ValueError(f'Derivative of n ^ x is undefined with n = {self.n}')
        return n_exp(self.n) * self.ln

    def __str__(self) -> str:
        return f'{self.n}^x'

    def __new__(cls, n):
        if n == 0 or n == 1:
            return const(n)
        return super(n_exp, cls).__new__(cls, n)

class log_base_n (ArithmeticOpBase):
    """Returns log_n(x) i.e. the argument to the log varies based on the input."""
    def __init__(self, n: number):
        super().__init__(n)
        if self.n <= 0:
            raise ValueError(f'Log base must be greater than 0, not {self.n}')
        self.ln = log(self.n)
        self.priority = 5

    def f(self, x: number) -> number:
        return log(x, self.n)

    def f_prime(self) -> ArithmeticOpBase:
        return const(1) / mult_n(self.ln)

    def __str__(self) -> str:
        if not isinstance(self.n, Fraction) and np.isclose(self.n, e):
            return 'ln(x)'
        return f'log{self.n}(x)'

class log_of_n (ArithmeticOpBase):
    """Returns log_x(n) i.e. the base of the log varies based on the input."""
    def __init__(self, n: number):
        super().__init__(n)
        if self.n <= 0:
            raise ValueError(f'Log argument must be greater than 0, not {self.n}')
        self.ln = log(self.n)
        self.priority = 5

    def f(self, x: number) -> number:
        return log(self.n, x)

    def f_prime(self) -> ArithmeticOpBase:
        return const(-self.ln) / (identity() * log_base_n(e) ** 2)
    
    def __str__(self) -> str:
        return f'log_x({self.n})'

    def __new__(cls, n):
        if n == 1:
            return const(0)
        return super(log_of_n, cls).__new__(cls, n)
